#!/usr/bin/env python3
"""Open SVGs in macOS Safari, screenshot them, and place each shot on a full-bleed picture slide."""

import argparse
import base64
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SLIDE_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
LAYOUT_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
IMAGE_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
REMOTE_AUTOMATION_HINT = """Safari 还不能被 WebDriver 控制。请任选一种方式打开后重跑，不要让助手代输密码：
1. 在「终端」执行 safaridriver --enable，并输入开机密码。
2. Safari → 设置 → 开发者 → 勾选「允许远程自动化」。没有「开发者」时，先到「设置 → 高级」打开「在菜单栏中显示开发菜单」。
"""


class SkillError(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def natural_key(path):
    pieces = []
    for part in re.split(r"(\d+)", path.name):
        if part.isdigit():
            pieces.append((0, int(part)))
        else:
            pieces.append((1, part.lower()))
    return pieces


def collect_svgs(inputs):
    found = []
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            files = [
                item for item in path.iterdir()
                if item.is_file() and item.suffix.lower() == ".svg" and not item.name.startswith(".")
            ]
            found.extend(sorted(files, key=natural_key))
        elif path.is_file() and path.suffix.lower() == ".svg":
            found.append(path)
        else:
            raise SkillError("不是 SVG 文件或文件夹: %s" % path)
    if not found:
        raise SkillError("没有找到 SVG。文件夹只读取当前这一层的 .svg 文件。")
    return found


def automation_pids():
    result = subprocess.run(
        ["pgrep", "-f", "MacOS/Safari --automation"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()
    return {int(line) for line in result.stdout.split() if line.strip().isdigit()}


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_port(port, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), 0.2):
                return
        except OSError:
            time.sleep(0.1)
    raise SkillError("safaridriver 没有在端口 %s 上启动。" % port)


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return


class SafariShots(object):
    def __init__(self):
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.driver = None
        self.httpd = None
        self.http_thread = None
        self.sid = None
        self.base = None
        self.serve_dir = None
        self.automation_before = automation_pids()
        self.fitted = False

    def close(self):
        if self.sid and self.base:
            try:
                self.call("DELETE", "/session/%s" % self.sid, timeout=8)
            except Exception:
                pass
            self.sid = None
        if self.httpd:
            try:
                self.httpd.shutdown()
            except Exception:
                pass
            self.httpd = None
        if self.driver and self.driver.poll() is None:
            self.driver.terminate()
            try:
                self.driver.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.driver.kill()
        self.driver = None
        deadline = time.time() + 2
        while time.time() < deadline:
            leftover = automation_pids() - self.automation_before
            if not leftover:
                break
            for pid in leftover:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
            time.sleep(0.2)

    def call(self, method, path, payload=None, timeout=30):
        data = None if payload is None else __import__("json").dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with self.opener.open(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
                return __import__("json").loads(raw) if raw else {}
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", "replace")
            if "remote automation" in body.lower():
                raise SkillError(REMOTE_AUTOMATION_HINT, code=2)
            raise SkillError("Safari WebDriver %s %s -> HTTP %s %s" % (method, path, error.code, body[:800]))
        except (socket.timeout, TimeoutError) as error:
            raise SkillError("Safari WebDriver 超时: %s %s" % (method, path)) from error

    def start(self, serve_dir):
        self.serve_dir = Path(serve_dir)
        port = free_port()
        handler = lambda *args, **kwargs: SilentHandler(*args, directory=str(self.serve_dir), **kwargs)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
        self.http_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.http_thread.start()
        self.http_port = port

        driver_port = free_port()
        self.base = "http://127.0.0.1:%s" % driver_port
        try:
            self.driver = subprocess.Popen(
                ["safaridriver", "-p", str(driver_port)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError:
            raise SkillError("找不到 safaridriver。")
        try:
            wait_port(driver_port)
        except SkillError:
            err = ""
            if self.driver.stderr:
                err = self.driver.stderr.read().decode("utf-8", "replace")[-500:]
            raise SkillError("safaridriver 启动失败。%s" % err)
        created = self.call(
            "POST",
            "/session",
            {
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "Safari",
                        "platformName": "macOS",
                        "pageLoadStrategy": "none",
                    }
                }
            },
            timeout=60,
        )
        value = created.get("value") or {}
        if isinstance(value, dict) and value.get("error"):
            message = value.get("message") or str(value)
            if "remote automation" in message.lower():
                raise SkillError(REMOTE_AUTOMATION_HINT, code=2)
            raise SkillError(message)
        self.sid = value.get("sessionId")
        if not self.sid:
            raise SkillError("没有拿到 Safari 会话: %s" % created)
        self.call(
            "POST",
            "/session/%s/timeouts" % self.sid,
            {"implicit": 0, "pageLoad": 5000, "script": 15000},
        )

    def drop_browser(self):
        if self.sid and self.base:
            try:
                self.call("DELETE", "/session/%s" % self.sid, timeout=5)
            except Exception:
                pass
        self.sid = None
        if self.driver and self.driver.poll() is None:
            self.driver.terminate()
            try:
                self.driver.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.driver.kill()
        self.driver = None
        self.fitted = False
        deadline = time.time() + 2
        while time.time() < deadline:
            leftover = automation_pids() - self.automation_before
            if not leftover:
                break
            for pid in leftover:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
            time.sleep(0.2)

    def reopen_browser(self):
        print("Safari 窗口断开，重新打开。", flush=True)
        self.drop_browser()
        driver_port = free_port()
        self.base = "http://127.0.0.1:%s" % driver_port
        self.driver = subprocess.Popen(
            ["safaridriver", "-p", str(driver_port)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        wait_port(driver_port)
        created = self.call(
            "POST",
            "/session",
            {
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "Safari",
                        "platformName": "macOS",
                        "pageLoadStrategy": "none",
                    }
                }
            },
            timeout=60,
        )
        value = created.get("value") or {}
        if isinstance(value, dict) and value.get("error"):
            message = value.get("message") or str(value)
            if "remote automation" in message.lower():
                raise SkillError(REMOTE_AUTOMATION_HINT, code=2)
            raise SkillError(message)
        self.sid = value.get("sessionId")
        if not self.sid:
            raise SkillError("没有拿到 Safari 会话: %s" % created)
        self.call(
            "POST",
            "/session/%s/timeouts" % self.sid,
            {"implicit": 0, "pageLoad": 5000, "script": 15000},
        )

    def js(self, script, timeout=12):
        result = self.call(
            "POST",
            "/session/%s/execute/sync" % self.sid,
            {"script": script, "args": []},
            timeout=timeout,
        )
        value = result.get("value")
        if isinstance(value, dict) and value.get("error"):
            raise SkillError("Safari 脚本失败: %s" % value.get("message", value))
        return value

    def open_svg(self, name):
        url = "http://127.0.0.1:%s/%s" % (self.http_port, name)
        self.call("POST", "/session/%s/url" % self.sid, {"url": url}, timeout=20)
        last = ""
        deadline = time.time() + 20
        while time.time() < deadline:
            try:
                last = self.js(
                    "return document.readyState + '|' + document.documentElement.tagName + '|' + location.pathname;"
                )
            except SkillError as error:
                if "超时" not in str(error):
                    raise
                time.sleep(0.4)
                continue
            if isinstance(last, str) and name in last and "|svg|" in last.lower() and last.startswith("complete"):
                return
            time.sleep(0.25)
        raise SkillError("Safari 没有打开 SVG: %s （%s）" % (name, last))

    def _window(self, rect):
        self.call("POST", "/session/%s/window/rect" % self.sid, rect)

    def _window_get(self):
        return self.call("GET", "/session/%s/window/rect" % self.sid)["value"]

    def fit_viewport(self):
        self._window({"x": 0, "y": 40, "width": 900, "height": 700})
        time.sleep(0.3)
        info = self.js(
            "return {sw: screen.availWidth, sh: screen.availHeight, iw: window.innerWidth, ih: window.innerHeight};"
        )
        self._window({"x": 0, "y": 0, "width": int(info["sw"]), "height": int(info["sh"])})
        time.sleep(0.35)
        info = self.js("return {sw: screen.availWidth, sh: screen.availHeight, iw: window.innerWidth, ih: window.innerHeight};")
        inner_w = int(info["iw"])
        inner_h = int(info["ih"])
        if inner_w < 320 or inner_h < 180:
            raise SkillError("Safari 视口过小: %sx%s" % (inner_w, inner_h))
        if inner_w / float(inner_h) > 16 / 9:
            view_h = inner_h
            view_w = int(inner_h * 16 / 9)
        else:
            view_w = inner_w
            view_h = int(inner_w * 9 / 16)
        view_w -= view_w % 2
        view_h -= view_h % 2
        rect = self._window_get()
        chrome_w = int(rect["width"]) - inner_w
        chrome_h = int(rect["height"]) - inner_h
        new_w = view_w + chrome_w
        new_h = view_h + chrome_h
        origin_y = 28 if 28 + new_h <= int(info["sh"]) + 80 else 0
        self._window({"x": 0, "y": origin_y, "width": new_w, "height": new_h})
        time.sleep(0.3)
        info = self.js("return {iw: window.innerWidth, ih: window.innerHeight};")
        rect = self._window_get()
        chrome_w = int(rect["width"]) - int(info["iw"])
        chrome_h = int(rect["height"]) - int(info["ih"])
        self._window(
            {
                "x": int(rect["x"]),
                "y": int(rect["y"]),
                "width": view_w + chrome_w,
                "height": view_h + chrome_h,
            }
        )
        time.sleep(0.25)
        self.fitted = True

    def paint_svg(self):
        sized = self.js(
            """
            const svg = document.documentElement;
            const w = window.innerWidth;
            const h = window.innerHeight;
            svg.setAttribute('width', String(w));
            svg.setAttribute('height', String(h));
            svg.style.display = 'block';
            svg.style.margin = '0';
            svg.style.overflow = 'hidden';
            return {w: w, h: h, sw: svg.scrollWidth, sh: svg.scrollHeight, dpr: window.devicePixelRatio};
            """
        )
        return sized

    def screenshot(self, dest):
        result = self.call("GET", "/session/%s/screenshot" % self.sid, timeout=60)
        png = base64.b64decode(result["value"])
        if not png.startswith(b"\x89PNG"):
            raise SkillError("Safari 截图不是 PNG: %s" % dest.name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(png)
        return dest

    def capture(self, svg_paths, out_dir):
        staging = Path(tempfile.mkdtemp(prefix="safari-svg-"))
        names = []
        try:
            for index, svg in enumerate(svg_paths, 1):
                name = "%04d.svg" % index
                os.symlink(svg.resolve(), staging / name)
                names.append(name)
            self.start(staging)
            shots = []
            used_names = set()
            for index, (svg, name) in enumerate(zip(svg_paths, names), 1):
                print("截图 %s/%s %s" % (index, len(svg_paths), svg.name), flush=True)
                shot_name = "%s.png" % svg.stem
                if shot_name in used_names:
                    shot_name = "%02d-%s.png" % (index, svg.stem)
                used_names.add(shot_name)
                dest = out_dir / shot_name
                attempts = 0
                while True:
                    try:
                        self.open_svg(name)
                        if not self.fitted:
                            self.fit_viewport()
                        sized = self.paint_svg()
                        time.sleep(0.35)
                        self.screenshot(dest)
                        break
                    except SkillError as error:
                        text = str(error)
                        if attempts < 2 and ("no such window" in text or "超时" in text):
                            attempts += 1
                            self.reopen_browser()
                            continue
                        raise
                print("  %sx%s dpr %s -> %s" % (sized.get("w"), sized.get("h"), sized.get("dpr"), dest), flush=True)
                shots.append(dest)
            return shots
        finally:
            self.close()
            shutil.rmtree(staging, ignore_errors=True)


def png_size(path):
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    width = int(re.search(r"pixelWidth: (\d+)", result.stdout).group(1))
    height = int(re.search(r"pixelHeight: (\d+)", result.stdout).group(1))
    return width, height


def crop_to_aspect(path, aspect):
    width, height = png_size(path)
    current = width / float(height)
    if abs(current - aspect) / aspect < 0.002:
        return
    if current > aspect:
        new_w = int(round(height * aspect))
        new_h = height
    else:
        new_w = width
        new_h = int(round(width / aspect))
    new_w -= new_w % 2
    new_h -= new_h % 2
    subprocess.check_call(["sips", "-c", str(new_h), str(new_w), str(path)], stdout=subprocess.DEVNULL)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, text):
    Path(path).write_text(text, encoding="utf-8")


def slide_size(pres_xml):
    match = re.search(r'<p:sldSz[^>]*cx="(\d+)"[^>]*cy="(\d+)"', pres_xml)
    if not match:
        raise SkillError("PPT 缺少幻灯片尺寸 p:sldSz。")
    return int(match.group(1)), int(match.group(2))


def presentation_rels(work):
    return work / "ppt" / "_rels" / "presentation.xml.rels"


def parse_rels(text):
    return re.findall(r'<Relationship\s+Id="([^"]+)"\s+Type="([^"]+)"\s+Target="([^"]+)"\s*/>', text)


def ordered_slides(work):
    pres = read_text(work / "ppt" / "presentation.xml")
    rels = dict((item[0], item[2]) for item in parse_rels(read_text(presentation_rels(work))) if item[1] == SLIDE_REL_TYPE)
    order = []
    for slide_id, rel_id in re.findall(r'<p:sldId id="(\d+)" r:id="(rId\d+)"/>', pres):
        target = rels.get(rel_id)
        if not target:
            raise SkillError("幻灯片关系缺失: %s" % rel_id)
        part = "ppt/" + target.lstrip("./")
        # Targets look like slides/slide1.xml
        if part.startswith("ppt/ppt/"):
            part = part[4:]
        order.append({"id": slide_id, "rel_id": rel_id, "part": part})
    return order


def sp_tree(xml):
    match = re.search(r"<p:spTree>(.*)</p:spTree>", xml, re.S)
    if not match:
        raise SkillError("幻灯片缺少 spTree。")
    return match.group(1)


def shape_blocks(xml):
    tree = sp_tree(xml)
    return re.findall(r"<p:(?:sp|pic|cxnSp|graphicFrame|grpSp)\b.*?</p:(?:sp|pic|cxnSp|graphicFrame|grpSp)>", tree, re.S)


def xfrm_xml(shape):
    match = re.search(r"<a:xfrm\b[^>]*>.*?</a:xfrm>", shape, re.S)
    return match.group(0) if match else None


def ph_identity(shape):
    match = re.search(r"<p:ph\b([^>]*)/>", shape)
    if not match:
        return None
    attrs = match.group(1)
    kind = re.search(r'type="([^"]+)"', attrs)
    index = re.search(r'idx="([^"]+)"', attrs)
    return (kind.group(1) if kind else "", index.group(1) if index else "")


def covers_slide(xfrm, slide_cx, slide_cy):
    ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', xfrm)
    if not ext:
        return False
    off = re.search(r'<a:off x="(\d+)" y="(\d+)"', xfrm)
    off_x = int(off.group(1)) if off else 0
    off_y = int(off.group(2)) if off else 0
    return (
        abs(off_x) <= 20000
        and abs(off_y) <= 20000
        and abs(int(ext.group(1)) - slide_cx) <= 20000
        and abs(int(ext.group(2)) - slide_cy) <= 20000
    )


def layout_xfrm(work, rels_text, shape):
    target = layout_target(rels_text)
    # Target is relative to the slide part, not the rels file.
    layout_path = (work / "ppt" / "slides" / target).resolve()
    if not layout_path.is_file():
        return None
    identity = ph_identity(shape)
    for block in shape_blocks(read_text(layout_path)):
        if ph_identity(block) == identity:
            return xfrm_xml(block)
    return None


def is_full_bleed(xml, slide_cx, slide_cy, fallback_xfrm=None):
    blocks = shape_blocks(xml)
    if len(blocks) != 1:
        return False
    shape = blocks[0]
    if not re.search(r'<p:ph\b[^>]*type="pic"', shape):
        return False
    xfrm = xfrm_xml(shape) or fallback_xfrm
    if not xfrm:
        return False
    return covers_slide(xfrm, slide_cx, slide_cy)


def build_pic(shape_xml, rel_id, fallback_xfrm=None):
    cnv = re.search(r"<p:cNvPr\b([^>]*)>", shape_xml)
    attrs = cnv.group(1) if cnv else ' id="2" name="Picture Placeholder 3"'
    creation = re.search(r"<a16:creationId\b[^>]*/>", shape_xml)
    creation_xml = ""
    if creation:
        creation_xml = (
            '<a:extLst><a:ext uri="{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}">'
            + creation.group(0)
            + "</a:ext></a:extLst>"
        )
    ph = re.search(r"<p:ph\b[^>]*/>", shape_xml)
    ph_tag = ph.group(0) if ph else '<p:ph type="pic" idx="1"/>'
    xfrm = xfrm_xml(shape_xml) or fallback_xfrm
    if not xfrm:
        raise SkillError("图片占位缺少位置。")
    return (
        "<p:pic><p:nvPicPr><p:cNvPr%s>%s</p:cNvPr>"
        '<p:cNvPicPr><a:picLocks noGrp="1" noChangeAspect="1"/></p:cNvPicPr>'
        "<p:nvPr>%s</p:nvPr></p:nvPicPr>"
        '<p:blipFill><a:blip r:embed="%s">'
        '<a:extLst><a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">'
        '<a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/>'
        "</a:ext></a:extLst></a:blip>"
        "<a:stretch><a:fillRect/></a:stretch></p:blipFill>"
        "<p:spPr>%s<a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></p:spPr></p:pic>"
    ) % (attrs, creation_xml, ph_tag, rel_id, xfrm)


def replace_shape(xml, new_shape):
    match = re.search(
        r"<p:(?:sp|pic)\b[^>]*>.*?</p:(?:sp|pic)>",
        xml,
        re.S,
    )
    if not match:
        raise SkillError("找不到可替换的图片占位。")
    return xml[: match.start()] + new_shape + xml[match.end() :]


def layout_target(rels_text):
    for _rel_id, rel_type, target in parse_rels(rels_text):
        if rel_type == LAYOUT_REL_TYPE:
            return target
    raise SkillError("幻灯片没有版式关系。")


def max_numeric(pattern, text):
    numbers = [int(item) for item in re.findall(pattern, text)]
    return max(numbers) if numbers else 0


def next_slide_number(work):
    numbers = []
    for path in (work / "ppt" / "slides").glob("slide*.xml"):
        match = re.fullmatch(r"slide(\d+)", path.stem)
        if match:
            numbers.append(int(match.group(1)))
    return (max(numbers) if numbers else 0) + 1


def ensure_png_default(work):
    path = work / "[Content_Types].xml"
    text = read_text(path)
    if 'Extension="png"' not in text:
        text = text.replace(
            "<Types ",
            '<Types ',
            1,
        )
        needle = "<Default "
        insert = '<Default Extension="png" ContentType="image/png"/>'
        if needle in text:
            text = text.replace(needle, insert + needle, 1)
        else:
            text = text.replace("</Types>", insert + "</Types>")
        write_text(path, text)


def add_slide_part(work, template_xml, template_rels):
    number = next_slide_number(work)
    part = "ppt/slides/slide%s.xml" % number
    (work / part).write_bytes(template_xml)
    rels_path = work / "ppt" / "slides" / "_rels" / ("slide%s.xml.rels" % number)
    rels_path.parent.mkdir(parents=True, exist_ok=True)
    rels_path.write_bytes(template_rels)

    content_types = work / "[Content_Types].xml"
    types = read_text(content_types)
    override = (
        '<Override PartName="/ppt/slides/slide%s.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        % number
    )
    if override not in types:
        types = types.replace("</Types>", override + "</Types>")
        write_text(content_types, types)

    rels_file = presentation_rels(work)
    rels = read_text(rels_file)
    rel_id = "rId%s" % (max_numeric(r'Id="rId(\d+)"', rels) + 1)
    relationship = (
        '<Relationship Id="%s" Type="%s" Target="slides/slide%s.xml"/>'
        % (rel_id, SLIDE_REL_TYPE, number)
    )
    write_text(rels_file, rels.replace("</Relationships>", relationship + "</Relationships>"))

    pres_path = work / "ppt" / "presentation.xml"
    pres = read_text(pres_path)
    slide_id = max_numeric(r'<p:sldId id="(\d+)"', pres) + 1
    sld = '<p:sldId id="%s" r:id="%s"/>' % (slide_id, rel_id)
    write_text(pres_path, pres.replace("</p:sldIdLst>", sld + "</p:sldIdLst>"))
    return part


def delete_slide_part(work, part):
    name = Path(part).name
    rels = read_text(presentation_rels(work))
    match_text = None
    rel_id = None
    for chunk in re.findall(r"<Relationship\b[^>]*/>", rels):
        if ('Target="slides/%s"' % name) in chunk and SLIDE_REL_TYPE in chunk:
            match_text = chunk
            rel_id = re.search(r'Id="(rId\d+)"', chunk).group(1)
            break
    if not rel_id:
        raise SkillError("找不到要删除的幻灯片关系: %s" % name)
    write_text(presentation_rels(work), rels.replace(match_text, "", 1))
    pres_path = work / "ppt" / "presentation.xml"
    pres = read_text(pres_path)
    pres = re.sub(r'<p:sldId id="\d+" r:id="%s"/>' % rel_id, "", pres)
    write_text(pres_path, pres)
    types_path = work / "[Content_Types].xml"
    types = read_text(types_path)
    types = re.sub(r'<Override PartName="/ppt/slides/%s"[^>]*/>' % re.escape(name), "", types)
    write_text(types_path, types)
    (work / part).unlink(missing_ok=True)
    rels_path = work / "ppt" / "slides" / "_rels" / (name + ".rels")
    rels_path.unlink(missing_ok=True)


def fill_slide(work, part, png_path):
    xml_path = work / part
    xml = read_text(xml_path)
    blocks = shape_blocks(xml)
    if len(blocks) != 1:
        raise SkillError("%s 不是单张全屏图片页。" % part)
    rels_path = work / "ppt" / "slides" / "_rels" / (Path(part).name + ".rels")
    rels = read_text(rels_path)
    layout = layout_target(rels)
    fallback = xfrm_xml(blocks[0]) or layout_xfrm(work, rels, blocks[0])
    image_rel = "rId2"
    used = {item[0] for item in parse_rels(rels)}
    if image_rel in used and image_rel == "rId1":
        image_rel = "rId3"
    media_name = "safari-%s.png" % Path(part).stem
    media_dir = work / "ppt" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(png_path, media_dir / media_name)
    new_xml = replace_shape(xml, build_pic(blocks[0], image_rel, fallback))
    write_text(xml_path, new_xml)
    write_text(
        rels_path,
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="%s" Target="%s"/>'
        '<Relationship Id="%s" Type="%s" Target="../media/%s"/>'
        "</Relationships>" % (LAYOUT_REL_TYPE, layout, image_rel, IMAGE_REL_TYPE, media_name),
    )


def cleanup_media(work):
    media = work / "ppt" / "media"
    if not media.exists():
        return
    referenced = set()
    for rels in work.rglob("*.rels"):
        for _rel_id, rel_type, target in parse_rels(read_text(rels)):
            if rel_type == IMAGE_REL_TYPE or "media/" in target:
                referenced.add(Path(target).name)
    for image in media.iterdir():
        if image.is_file() and image.name not in referenced:
            image.unlink()


def update_app_xml(work, slide_count):
    path = work / "docProps" / "app.xml"
    if not path.exists():
        return
    text = read_text(path)
    text = re.sub(r"<Slides>\d+</Slides>", "<Slides>%s</Slides>" % slide_count, text, count=1)
    text = re.sub(
        r"(<vt:lpstr>Slide Titles</vt:lpstr></vt:variant><vt:variant><vt:i4>)\d+(</vt:i4>)",
        lambda match: match.group(1) + str(slide_count) + match.group(2),
        text,
        count=1,
    )
    titles = re.search(r'(<TitlesOfParts><vt:vector size=")\d+(" baseType="lpstr">)(.*?)(</vt:vector>)', text, re.S)
    fonts = re.search(r"Fonts Used</vt:lpstr></vt:variant><vt:variant><vt:i4>(\d+)", text)
    themes = re.search(r"Theme</vt:lpstr></vt:variant><vt:variant><vt:i4>(\d+)", text)
    if titles and fonts and themes:
        items = re.findall(r"<vt:lpstr>.*?</vt:lpstr>", titles.group(3))
        head_count = int(fonts.group(1)) + int(themes.group(1))
        if head_count <= len(items):
            head = items[:head_count]
            names = items[head_count:]
            while len(names) < slide_count:
                names.append("<vt:lpstr>PowerPoint Presentation</vt:lpstr>")
            names = names[:slide_count]
            replacement = "".join(head + names)
            text = (
                text[: titles.start()]
                + titles.group(1)
                + str(len(head) + len(names))
                + titles.group(2)
                + replacement
                + titles.group(4)
                + text[titles.end() :]
            )
    write_text(path, text)


def unpack_pptx(pptx_path, work):
    subprocess.check_call(["unzip", "-q", "-o", str(pptx_path), "-d", str(work)])


def pack_pptx(work, dest):
    for junk in work.rglob(".DS_Store"):
        junk.unlink()
    for xml_path in list(work.rglob("*.xml")) + list(work.rglob("*.rels")):
        ET.parse(str(xml_path))
    packed = Path(tempfile.mkdtemp(prefix="pptx-pack-")) / "out.pptx"
    subprocess.check_call(["zip", "-Xr", str(packed), "."], cwd=str(work), stdout=subprocess.DEVNULL)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp_dest = dest.with_name(dest.name + ".writing")
    shutil.copyfile(packed, tmp_dest)
    shutil.rmtree(packed.parent, ignore_errors=True)
    try:
        os.replace(tmp_dest, dest)
    except OSError:
        fallback = dest.with_name(dest.stem + ".safari.pptx")
        os.replace(tmp_dest, fallback)
        raise SkillError("无法覆盖 %s，已另存为 %s。若 PPT 正打开，请先关闭再替换。" % (dest, fallback))


def load_slide_records(work):
    pres = read_text(work / "ppt" / "presentation.xml")
    slide_cx, slide_cy = slide_size(pres)
    records = []
    for item in ordered_slides(work):
        xml = read_text(work / item["part"])
        rels_path = work / "ppt" / "slides" / "_rels" / (Path(item["part"]).name + ".rels")
        rels = read_text(rels_path) if rels_path.is_file() else ""
        blocks = shape_blocks(xml)
        fallback = None
        if len(blocks) == 1 and not xfrm_xml(blocks[0]) and rels:
            fallback = layout_xfrm(work, rels, blocks[0])
        item["full_bleed"] = is_full_bleed(xml, slide_cx, slide_cy, fallback)
        records.append(item)
    return records, slide_cx, slide_cy


def apply_screenshots(pptx_path, png_paths, output_path):
    pptx_path = Path(pptx_path)
    output_path = Path(output_path)
    png_paths = [Path(path) for path in png_paths]
    if not pptx_path.is_file():
        raise SkillError("找不到 PPT: %s" % pptx_path)
    work = Path(tempfile.mkdtemp(prefix="pptx-safari-"))
    try:
        unpack_pptx(pptx_path, work)
        records, slide_cx, slide_cy = load_slide_records(work)
        if not records:
            raise SkillError("PPT 里没有幻灯片。")
        full = [item for item in records if item["full_bleed"]]
        if not full:
            raise SkillError("这份 PPT 里没有铺满全屏的图片页，不能当作空白页模板。")
        all_full = len(full) == len(records)
        template_part = full[0]["part"]
        template_xml = (work / template_part).read_bytes()
        template_rels = (work / "ppt" / "slides" / "_rels" / (Path(template_part).name + ".rels")).read_bytes()
        aspect = slide_cx / float(slide_cy)
        for png in png_paths:
            crop_to_aspect(png, aspect)

        targets = [item["part"] for item in full]
        if all_full:
            while len(targets) > len(png_paths):
                delete_slide_part(work, targets.pop())
            while len(targets) < len(png_paths):
                targets.append(add_slide_part(work, template_xml, template_rels))
        else:
            while len(targets) < len(png_paths):
                targets.append(add_slide_part(work, template_xml, template_rels))
            targets = targets[: len(png_paths)]

        ensure_png_default(work)
        for part, png in zip(targets, png_paths):
            fill_slide(work, part, png)
        cleanup_media(work)
        final_count = len(ordered_slides(work))
        update_app_xml(work, final_count)
        pack_pptx(work, output_path)
        return {"slides": final_count, "filled": [Path(part).name for part in targets]}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def print_plan(svg_paths, pptx_path):
    work = Path(tempfile.mkdtemp(prefix="pptx-plan-"))
    try:
        unpack_pptx(pptx_path, work)
        records, slide_cx, slide_cy = load_slide_records(work)
        full = [item for item in records if item["full_bleed"]]
        all_full = bool(records) and len(full) == len(records)
        print("PPT: %s" % pptx_path)
        print("幻灯片尺寸 EMU: %s x %s" % (slide_cx, slide_cy))
        print("现有页数: %s，其中全屏图片页: %s" % (len(records), len(full)))
        print("整份都是全屏图片页: %s" % ("是" if all_full else "否"))
        if not full:
            print("无法写入：没有铺满全屏的图片页。")
            return 1
        print("SVG %s 张:" % len(svg_paths))
        existing = len(full)
        for index, svg in enumerate(svg_paths, 1):
            if index <= existing:
                part = full[index - 1]["part"]
                action = "写入 %s" % Path(part).name
            else:
                action = "按空白页模板追加"
            print("  %02d  %s  ->  %s" % (index, svg.name, action))
        if all_full and existing > len(svg_paths):
            for item in full[len(svg_paths) :]:
                print("  删除多余空白页 %s" % Path(item["part"]).name)
        elif not all_full and existing > len(svg_paths):
            print("  其余内容页和未用到的全屏图片页保留。")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="用 Safari 截取 SVG，并写入 PPT 的全屏图片页。")
    parser.add_argument("--svg", action="append", required=True, help="SVG 文件或文件夹，可重复")
    parser.add_argument("--pptx", required=True, help="已有全屏图片空白页的 PPTX")
    parser.add_argument("--output", help="输出 PPTX，默认覆盖 --pptx")
    parser.add_argument("--dry-run", action="store_true", help="只打印页序，不打开 Safari，不写 PPT")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    try:
        svgs = collect_svgs(args.svg)
        pptx_path = Path(args.pptx).expanduser().resolve()
        if not pptx_path.is_file():
            raise SkillError("找不到 PPT: %s" % pptx_path)
        if args.dry_run:
            return print_plan(svgs, pptx_path)
        output = Path(args.output).expanduser().resolve() if args.output else pptx_path
        capture_dir = output.parent / "safari-captures"
        capture_dir.mkdir(parents=True, exist_ok=True)
        shots = SafariShots().capture(svgs, capture_dir)
        result = apply_screenshots(pptx_path, shots, output)
        print("已写入 %s" % output)
        print("共 %s 页，本次放入 %s 张全屏图片。" % (result["slides"], len(result["filled"])))
        for svg, shot, part in zip(svgs, shots, result["filled"]):
            print("  %s -> %s -> %s" % (svg.name, shot.name, part))
        return 0
    except SkillError as error:
        print(error, file=sys.stderr)
        return error.code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
