#!/usr/bin/env python3
"""
Fast automated Jianying Pro (剪映专业版) caption workflow for Antigravity.
Executes the entire caption pipeline in a single process using AXUIElement + pixel verification:
  1. New Draft (新建草稿)
  2. Import Video & Drag to Timeline (导入视频并入轨)
  3. Auto Caption Recognition (智能识别字幕)
  4. Apply Yellow-Background Black-Text Preset to All Captions (黄底黑字预设应用到全部字幕)
  5. Export <stem>_字幕版.mp4 and wait for 导出成功
"""

import os
import struct
import subprocess
import sys
import tempfile
import time


def collect_ax_nodes(cua, elem, depth=0, max_depth=10, results=None):
    if results is None:
        results = []
    if depth > max_depth or len(results) > 2000:
        return results

    role = cua.ax_get_str(elem, "AXRole") or "Unknown"
    if role == "AXMenuBar":
        return results

    title = cua.ax_get_str(elem, "AXTitle") or ""
    desc = cua.ax_get_str(elem, "AXDescription") or ""
    val = cua.ax_get_str(elem, "AXValue")
    val_str = str(val) if val is not None else ""
    pos = cua.ax_get_point(elem)
    size = cua.ax_get_size(elem)
    center = None
    if pos and size:
        center = (round(pos[0] + size[0] / 2.0, 1), round(pos[1] + size[1] / 2.0, 1))

    results.append({
        "role": role,
        "title": title,
        "desc": desc,
        "val": val_str,
        "pos": pos,
        "size": size,
        "center": center,
    })

    res = cua.ax_get_children(elem, "AXChildren")
    if res is not None:
        children, arr_ref = res
        for c in children:
            collect_ax_nodes(cua, c, depth + 1, max_depth, results)
        cua.cf.CFRelease(arr_ref)
    return results


def get_app_nodes(cua, max_depth=8):
    pid = cua.get_jianying_pid()
    if not pid:
        return []
    app_elem = cua.ax.AXUIElementCreateApplication(pid)
    nodes = collect_ax_nodes(cua, app_elem, max_depth=max_depth)
    cua.cf.CFRelease(app_elem)
    return nodes


def find_node(nodes, predicate):
    for n in nodes:
        if n["center"] and predicate(n):
            return n
    return None


def find_nodes(nodes, predicate):
    return [n for n in nodes if n["center"] and predicate(n)]


def find_yellow_preset_center(cua, search_rect=(1315, 280, 70, 330)):
    """
    Locate the 3rd-row 1st-column Yellow-Background Black-Text (黄底黑字) preset button
    inside the right panel by scanning Column 1 (x ≈ 1340) for its solid bright-yellow
    rounded square (~36x36 px of R>200, G>175, B<60).
    Returns (screen_x, screen_y) or None.
    """
    rx, ry, rw, rh = search_rect
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f_png:
        png_path = f_png.name
    bmp_path = png_path + ".bmp"
    try:
        cua.cmd_screenshot(png_path, rect_str=f"{rx},{ry},{rw},{rh}")
        subprocess.run(
            ["sips", "-s", "format", "bmp", png_path, "--out", bmp_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        with open(bmp_path, "rb") as f:
            data = f.read()
        if len(data) < 54 or data[:2] != b"BM":
            return None
        pixel_offset = struct.unpack_from("<I", data, 10)[0]
        width, height = struct.unpack_from("<ii", data, 18)
        bpp = struct.unpack_from("<H", data, 28)[0]
        top_down = height < 0
        height = abs(height)
        bytes_per_px = bpp // 8
        row_stride = ((width * bytes_per_px + 3) // 4) * 4

        yellow_rows = []
        for y in range(height):
            bmp_y = y if top_down else (height - 1 - y)
            row_start = pixel_offset + bmp_y * row_stride
            yellow_cnt = 0
            for x in range(width):
                px = row_start + x * bytes_per_px
                if px + 3 > len(data):
                    continue
                b, g, r = data[px], data[px + 1], data[px + 2]
                if r > 200 and g > 175 and b < 65:
                    yellow_cnt += 1
            # The solid yellow preset icon is ~36px wide, so a horizontal slice has >= 18 yellow pixels
            if yellow_cnt >= 16:
                yellow_rows.append(y)

        # Find a contiguous vertical band of at least 20 rows (the 36x36 solid yellow box)
        if not yellow_rows:
            return None
        bands = []
        cur = [yellow_rows[0]]
        for y in yellow_rows[1:]:
            if y <= cur[-1] + 3:
                cur.append(y)
            else:
                bands.append(cur)
                cur = [y]
        bands.append(cur)
        valid_bands = [b for b in bands if (b[-1] - b[0] + 1) >= 20]
        if not valid_bands:
            return None
        # Pick the solid yellow band
        target_band = valid_bands[0]
        cy_local = (target_band[0] + target_band[-1]) / 2.0
        return (1340.0, round(ry + cy_local, 1))
    finally:
        for p in (png_path, bmp_path):
            if os.path.exists(p):
                os.remove(p)


def run_auto_caption(cua, video_path: str, verify_dir: str = None, overwrite: bool = False):
    t_start = time.time()
    video_path = os.path.abspath(video_path)
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    video_dir = os.path.dirname(video_path)
    video_filename = os.path.basename(video_path)
    stem, _ = os.path.splitext(video_filename)
    target_stem = f"{stem}_字幕版"
    output_path = os.path.join(video_dir, f"{target_stem}.mp4")

    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError(
            f"Target output already exists (refusing to overwrite without --overwrite): {output_path}"
        )

    print(f"[0.0s] Starting fast auto-caption pipeline for: {video_path}")
    print(f"       Target output: {output_path}")

    # --- STEP 1: Activate Jianying Pro & Prepare Empty Draft ---
    t0 = time.time()
    cua.cmd_activate()
    nodes = get_app_nodes(cua, max_depth=6)

    # Wait up to 10s if app just launched and windows are still loading
    for _ in range(20):
        if len(nodes) > 5:
            break
        time.sleep(0.5)
        nodes = get_app_nodes(cua, max_depth=6)

    # Close any leftover ExportDialog if present
    exp_dlg = find_node(nodes, lambda n: n["desc"] == "ExportDialog")
    if exp_dlg:
        close_btn = find_node(nodes, lambda n: n["title"] in ("automationcloseBtn", "automationcancel"))
        if close_btn:
            print(f"[{time.time() - t_start:.1f}s] Closing previous ExportDialog at {close_btn['center']}")
            cua.mouse_click(*close_btn["center"])
            time.sleep(0.6)
            nodes = get_app_nodes(cua, max_depth=6)

    timeline_root = find_node(nodes, lambda n: n["desc"] == "MainTimeLineRoot")
    home_new = find_node(nodes, lambda n: n["desc"] in ("HomePageStartProjectDesp", "HomePageNewProject"))
    target_video_track = find_node(nodes, lambda n: n["desc"] == f"MTLSVideoP:{video_filename}")

    if not timeline_root and home_new:
        print(f"[{time.time() - t_start:.1f}s] Step 1/5: Clicking '开始创作' on Home Screen at {home_new['center']}")
        cua.mouse_click(*home_new["center"])
    elif timeline_root:
        has_video = find_node(nodes, lambda n: n["desc"].startswith("MTLSVideoP:"))
        if target_video_track:
            print(f"[{time.time() - t_start:.1f}s] Step 1/5: Reusing current draft that already has {target_video_track['desc']}")
        elif has_video:
            print(f"[{time.time() - t_start:.1f}s] Step 1/5: Existing draft has other video ({has_video['desc']}); creating new draft via 文件 -> 新建草稿")
            cua.mouse_click(115, 14)
            time.sleep(0.4)
            cua.mouse_click(135, 42)
        else:
            print(f"[{time.time() - t_start:.1f}s] Step 1/5: Reusing already open empty editor draft")

    # Wait until editor window is ready
    if not target_video_track:
        for _ in range(30):
            time.sleep(0.5)
            nodes = get_app_nodes(cua, max_depth=6)
            timeline_root = find_node(nodes, lambda n: n["desc"] == "MainTimeLineRoot")
            has_video = find_node(nodes, lambda n: n["desc"].startswith("MTLSVideoP:"))
            if timeline_root and not has_video:
                break
    if not timeline_root:
        raise RuntimeError("Failed to open Jianying Editor window (MainTimeLineRoot not found).")
    print(f"[{time.time() - t_start:.1f}s] Step 1/5 complete ({time.time() - t0:.1f}s): Draft ready.")

    # --- STEP 2: Import Video & Add to Timeline ---
    t0 = time.time()
    video_track = find_node(nodes, lambda n: n["desc"] == f"MTLSVideoP:{video_filename}")
    if not video_track:
        is_clip_node = lambda n: (n["desc"] == f"Name:{video_filename}") or (f".{video_filename}.apply" in (n["title"] + n["desc"]))
        clip_node = find_node(nodes, is_clip_node)
        if not clip_node:
            is_import_btn = lambda n: ("barImportViewBtn" in (n["title"] + n["desc"])) or ("ImportMainButton" in (n["title"] + n["desc"]))
            import_btn = find_node(nodes, is_import_btn)
            if not import_btn:
                media_tab = find_node(nodes, lambda n: n["desc"] == "root_素材")
                if media_tab:
                    cua.mouse_click(*media_tab["center"])
                    time.sleep(0.5)
                    nodes = get_app_nodes(cua, max_depth=6)
                    import_btn = find_node(nodes, is_import_btn)

            if not import_btn:
                raise RuntimeError("Could not find barImportViewBtn_ / ImportMainButton in Media panel.")

            # Check if NSOpenPanel (width=880) or Go-To-Folder popover (width=460) is already open
            cua.cg.CGWindowListCopyWindowInfo.argtypes = [cua.ctypes.c_uint32, cua.ctypes.c_uint32]
            cua.cg.CGWindowListCopyWindowInfo.restype = cua.ctypes.c_void_p
            cua.cf.CFDictionaryGetValue.argtypes = [cua.ctypes.c_void_p, cua.ctypes.c_void_p]
            cua.cf.CFDictionaryGetValue.restype = cua.ctypes.c_void_p

            def get_jy_win_widths():
                pid = cua.get_jianying_pid()
                arr = cua.cg.CGWindowListCopyWindowInfo(1, 0)
                if not arr:
                    return set()
                cnt = cua.cf.CFArrayGetCount(arr)
                widths = set()
                for i in range(cnt):
                    d = cua.cf.CFArrayGetValueAtIndex(arr, i)
                    wpid = cua.cf_to_py(cua.cf.CFDictionaryGetValue(d, cua.cfstr("kCGWindowOwnerPID")))
                    if wpid == float(pid):
                        b = cua.cf.CFDictionaryGetValue(d, cua.cfstr("kCGWindowBounds"))
                        w = int(cua.cf_to_py(cua.cf.CFDictionaryGetValue(b, cua.cfstr("Width"))) or 0)
                        widths.add(w)
                cua.cf.CFRelease(arr)
                return widths

            win_widths = get_jy_win_widths()
            if 880 not in win_widths:
                print(f"[{time.time() - t_start:.1f}s] Step 2/5: Clicking ImportMainButton at {import_btn['center']}")
                cua.mouse_click(*import_btn["center"], focus_first=False)
                time.sleep(1.5)
                win_widths = get_jy_win_widths()

            if 460 not in win_widths:
                cua.send_key("cmd+shift+g", focus_first=False)
                time.sleep(0.8)

            # Click the X clear button in Go-To-Folder popover at (1071, 424) and type UTF-16 path directly
            cua.mouse_click(1071.0, 424.0, focus_first=False)
            time.sleep(0.25)
            cua.type_unicode(video_path, press_enter=False, focus_first=False)
            time.sleep(0.7)
            cua.send_key("return", focus_first=False)
            time.sleep(0.9)
            cua.send_key("return", focus_first=False)

            for _ in range(25):
                time.sleep(0.5)
                nodes = get_app_nodes(cua, max_depth=7)
                clip_node = find_node(nodes, is_clip_node)
                if clip_node:
                    break
            if not clip_node:
                raise RuntimeError(f"Imported clip '{video_filename}' did not appear in media bin.")

        timeline_root = find_node(nodes, lambda n: n["desc"] == "MainTimeLineRoot")
        if clip_node["size"] and clip_node["size"][1] >= 35:
            drag_src = (200.0, clip_node["center"][1])
        else:
            drag_src = (clip_node["center"][0], clip_node["center"][1] - 32.0)
        drag_dst = (min(timeline_root["center"][0], 500.0), timeline_root["center"][1])
        print(f"[{time.time() - t_start:.1f}s] Dragging clip from {drag_src} to timeline {drag_dst}")
        cua.mouse_drag(drag_src[0], drag_src[1], drag_dst[0], drag_dst[1], duration=0.5)

        for _ in range(20):
            time.sleep(0.4)
            nodes = get_app_nodes(cua, max_depth=7)
            video_track = find_node(nodes, lambda n: n["desc"].startswith("MTLSVideoP:"))
            if video_track:
                break
        if not video_track:
            raise RuntimeError("Video track (MTLSVideoP) did not appear on timeline after drag.")
    print(f"[{time.time() - t_start:.1f}s] Step 2/5 complete ({time.time() - t0:.1f}s): Video on timeline ({video_track['desc']}).")

    # --- STEP 3: Auto Caption Recognition (智能识别字幕) ---
    t0 = time.time()
    caption_nodes = find_nodes(nodes, lambda n: n["desc"].startswith("MTLSTextP:") and 180 <= n["center"][0] <= 1650)
    if not caption_nodes:
        caption_tab = find_node(nodes, lambda n: n["desc"] == "root_字幕")
        if not caption_tab:
            raise RuntimeError("Could not find 'root_字幕' tab.")
        cua.mouse_click(*caption_tab["center"])
        time.sleep(0.6)
        nodes = get_app_nodes(cua, max_depth=7)

        rec_btn = find_node(nodes, lambda n: n["title"] == "开始识别" or n["val"] == "开始识别")
        if not rec_btn:
            sub_tab = find_node(nodes, lambda n: n["val"] == "识别字幕" or n["desc"] == "识别字幕")
            if sub_tab:
                cua.mouse_click(*sub_tab["center"])
                time.sleep(0.5)
                nodes = get_app_nodes(cua, max_depth=7)
                rec_btn = find_node(nodes, lambda n: n["title"] == "开始识别" or n["val"] == "开始识别")

        rec_pt = rec_btn["center"] if rec_btn else (488.0, 610.0)
        print(f"[{time.time() - t_start:.1f}s] Step 3/5: Clicking '开始识别' at {rec_pt} and polling for captions...")
        cua.mouse_click(*rec_pt)

        for i in range(300):
            time.sleep(1.0)
            nodes = get_app_nodes(cua, max_depth=7)
            caption_nodes = find_nodes(nodes, lambda n: n["desc"].startswith("MTLSTextP:") and 180 <= n["center"][0] <= 1650)
            if caption_nodes:
                time.sleep(0.8)
                nodes = get_app_nodes(cua, max_depth=7)
                caption_nodes = find_nodes(nodes, lambda n: n["desc"].startswith("MTLSTextP:") and 180 <= n["center"][0] <= 1650)
                break
            if (i + 1) % 10 == 0:
                print(f"[{time.time() - t_start:.1f}s]   ... still recognizing captions ({i + 1}s elapsed)")

    if not caption_nodes:
        raise RuntimeError("Auto caption recognition timed out or produced 0 caption segments.")
    print(f"[{time.time() - t_start:.1f}s] Step 3/5 complete ({time.time() - t0:.1f}s): Recognized {len(caption_nodes)} visible caption segments.")

    # --- STEP 4: Apply Yellow-Background Black-Text Preset to All Captions ---
    t0 = time.time()
    first_cap = caption_nodes[0]
    cx, cy = first_cap["center"]
    # Move playhead to first caption & select it
    cua.mouse_click(cx, 675)
    time.sleep(0.25)
    cua.mouse_click(cx, cy)
    time.sleep(0.6)
    nodes = get_app_nodes(cua, max_depth=9)

    apply_all = find_node(nodes, lambda n: "applyToAll" in (n["title"] + n["desc"]))
    if apply_all and apply_all["val"] in ("0", "0.0", "False"):
        print(f"[{time.time() - t_start:.1f}s] Checking '应用到全部字幕' at {apply_all['center']}")
        cua.mouse_click(*apply_all["center"])
        time.sleep(0.3)

    # Gently position '预设样式' into the upper-middle of the right panel (320 <= y <= 430) without overscrolling
    for _ in range(6):
        preset_label = find_node(nodes, lambda n: n["val"] == "预设样式")
        if preset_label and 320 <= preset_label["center"][1] <= 430:
            break
        if not preset_label or preset_label["center"][1] < 320:
            # Scrolled too far down; scroll back up slightly
            cua.mouse_scroll(1500, 450, 20)
        else:
            # Initial state (y ~ 480..580); scroll down 1 notch at a time
            cua.mouse_scroll(1500, 450, -30)
        time.sleep(0.2)
        nodes = get_app_nodes(cua, max_depth=9)

    preset_label = find_node(nodes, lambda n: n["val"] == "预设样式")
    preset_pt = find_yellow_preset_center(cua, search_rect=(1315, 280, 70, 310))
    if not preset_pt:
        # 预设样式 defaults to collapsed (hiding Row 3); click its bottom-center ▼ expand arrow at (1513.5, preset_label_y + 114)
        expand_y = (preset_label["center"][1] + 114.0) if preset_label else 505.0
        print(f"[{time.time() - t_start:.1f}s] Expanding '预设样式' panel via ▼ arrow at (1513.5, {expand_y})")
        cua.mouse_click(1513.5, expand_y)
        time.sleep(0.45)
        preset_pt = find_yellow_preset_center(cua, search_rect=(1315, 280, 70, 310))
        if not preset_pt:
            nodes = get_app_nodes(cua, max_depth=9)
            style_items = find_nodes(nodes, lambda n: n["desc"] == "automationstyleIconRepeaterItem")
            if len(style_items) >= 17:
                preset_pt = style_items[16]["center"]

    if not preset_pt:
        raise RuntimeError("Could not visually locate the Yellow-Background Black-Text preset in right panel.")

    print(f"[{time.time() - t_start:.1f}s] Step 4/5: Clicking Yellow-Background Black-Text preset at {preset_pt}")
    cua.mouse_click(*preset_pt)
    time.sleep(0.6)
    print(f"[{time.time() - t_start:.1f}s] Step 4/5 complete ({time.time() - t0:.1f}s): Preset applied to all captions.")

    # --- STEP 5: Export <stem>_字幕版.mp4 ---
    t0 = time.time()
    nodes = get_app_nodes(cua, max_depth=6)
    export_top_btn = find_node(nodes, lambda n: n["title"] == "MainWindowTitleBarExportBtn" or n["desc"] == "MainWindowTitleBarExportBtn")
    if not export_top_btn:
        raise RuntimeError("Could not find top-right MainWindowTitleBarExportBtn.")

    print(f"[{time.time() - t_start:.1f}s] Step 5/5: Opening Export dialog via {export_top_btn['center']}")
    cua.mouse_click(*export_top_btn["center"])

    fname_input = None
    ok_btn = None
    for _ in range(20):
        time.sleep(0.4)
        nodes = get_app_nodes(cua, max_depth=6)
        fname_input = find_node(nodes, lambda n: n["desc"] == "ExportFileNameInput")
        ok_btn = find_node(nodes, lambda n: n["title"] == "ExportOkBtn" or n["desc"] == "ExportOkBtn")
        if fname_input and ok_btn:
            break

    if not fname_input or not ok_btn:
        raise RuntimeError("Export dialog inputs (ExportFileNameInput / ExportOkBtn) did not appear.")

    # Check if export directory matches video_dir
    path_node = find_node(nodes, lambda n: n["desc"].endswith(".mp4") and "/" in n["desc"])
    if path_node:
        cur_dir = os.path.dirname(path_node["desc"])
        if os.path.abspath(cur_dir) != os.path.abspath(video_dir):
            folder_btn = find_node(nodes, lambda n: "ExportFileNameInputBtn" in (n["title"] + n["desc"]))
            if folder_btn:
                print(f"[{time.time() - t_start:.1f}s] Updating export directory from {cur_dir} to {video_dir}")
                cua.mouse_click(*folder_btn["center"], focus_first=False)
                time.sleep(1.4)
                cua.send_key("cmd+shift+g", focus_first=False)
                time.sleep(0.8)
                cua.mouse_click(1071.0, 424.0, focus_first=False)
                time.sleep(0.25)
                cua.type_unicode(video_dir, press_enter=False, focus_first=False)
                time.sleep(0.7)
                cua.send_key("return", focus_first=False)
                time.sleep(0.8)
                cua.send_key("return", focus_first=False)
                time.sleep(0.6)
                nodes = get_app_nodes(cua, max_depth=6)
                fname_input = find_node(nodes, lambda n: n["desc"] == "ExportFileNameInput")
                ok_btn = find_node(nodes, lambda n: n["title"] == "ExportOkBtn" or n["desc"] == "ExportOkBtn")

    print(f"[{time.time() - t_start:.1f}s] Setting export title to '{target_stem}' at {fname_input['center']}")
    cua.mouse_click(*fname_input["center"], count=3, focus_first=False)
    time.sleep(0.2)
    cua.send_key("delete", focus_first=False)
    time.sleep(0.15)
    cua.type_unicode(target_stem, press_enter=False, focus_first=False)
    time.sleep(0.4)

    nodes = get_app_nodes(cua, max_depth=6)
    fname_after = find_node(nodes, lambda n: n["desc"] == "ExportFileNameInput")
    print(f"[{time.time() - t_start:.1f}s] Verified export title input: {fname_after['val'] if fname_after else 'unknown'}")

    print(f"[{time.time() - t_start:.1f}s] Clicking ExportOkBtn at {ok_btn['center']} and waiting for 导出成功...")
    cua.mouse_click(*ok_btn["center"])

    export_done = False
    for i in range(600):
        time.sleep(1.0)
        nodes = get_app_nodes(cua, max_depth=6)
        pub_btn = find_node(nodes, lambda n: n["title"] == "publish_pc_btn" or n["desc"] == "publish_pc_btn")
        if pub_btn and os.path.isfile(output_path) and os.path.getsize(output_path) > 0:
            export_done = True
            break
        if (i + 1) % 10 == 0:
            print(f"[{time.time() - t_start:.1f}s]   ... exporting video ({i + 1}s elapsed)")

    if not export_done:
        raise RuntimeError("Export timed out before 导出成功 screen and output file appeared.")

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[{time.time() - t_start:.1f}s] Step 5/5 complete ({time.time() - t0:.1f}s): Export succeeded! ({size_mb:.1f} MB)")

    if verify_dir:
        os.makedirs(verify_dir, exist_ok=True)
        shot_path = os.path.join(verify_dir, f"{stem}_export_success.png")
        cua.cmd_screenshot(shot_path, rect_str="540,360,650,430")
        frame_path = os.path.join(verify_dir, f"{stem}_verify_frame.png")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", "00:00:05", "-i", output_path, "-frames:v", "1", frame_path, "-loglevel", "error"],
            check=False
        )
        print(f"[{time.time() - t_start:.1f}s] Saved verification artifacts to: {verify_dir}")

    print(f"DONE in {time.time() - t_start:.1f}s -> {output_path}")
    return output_path
