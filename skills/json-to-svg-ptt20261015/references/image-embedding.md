# 图片定位与 SVG 内嵌

仅在 JSON 有图片提示（如 `图片（使用附件中图片：xxx）`）或当前页有非空 `asset_refs` 时读取并执行。

## 定位与展示

- 查阅大纲同目录的 `outline-info.json`，以当前页的 `asset_refs` 匹配顶层 `assets`，取得 `path` 与 `original_reference`；缺少映射时沿图片提示回查原文附件。
- 必须检查真实文件存在，核对原文引用及目录、文件名空格（如 `pictures/`、`picture/`、`assets/`）。必须使用原文真实图片，严禁手绘替代或空白、文字占位；缺图时说明缺失引用，取得正确资源后再交付该页。
- 所有图片以 Base64 Data URI 内嵌，最终不得保留外部相对路径、绝对路径或网络地址，避免 QuickLook、IDE、浏览器预览拦截及目录变动导致失效。
- `<svg>` 声明 `xmlns="http://www.w3.org/2000/svg"` 和 `xmlns:xlink="http://www.w3.org/1999/xlink"`；`<image>` 设置 `preserveAspectRatio="xMidYMid meet"`。
- 白底图表建议使用浅色/白色内衬底板（如 `#ffffff`）和圆角 `clipPath`，确保深色主题下清晰可读，不裁去图例、坐标轴或注释。

## 内嵌与校验

先生成完整 SVG，在图片 `href` 或 `xlink:href` 中写唯一占位符，随即用 Python 读取真实图片并替换，避免手写 Base64 截断。替换下例路径；多图时扩展 `image_files`，不要打印完整 Base64。

```bash
python3 - <<'PY'
import base64, mimetypes, re, xml.etree.ElementTree as ET
from pathlib import Path

svg_file = Path("path/to/page-XXX.svg")
image_files = {"__IMAGE_ASSET_1__": Path("path/to/actual_image.png")}
text = svg_file.read_text(encoding="utf-8")
for marker, image_file in image_files.items():
    assert image_file.is_file(), f"Image not found: {image_file}"
    assert marker in text, f"Placeholder not found: {marker}"
    mime = mimetypes.guess_type(image_file.name)[0]
    assert mime and mime.startswith("image/"), f"Unknown image type: {image_file}"
    raw = image_file.read_bytes()
    assert raw, f"Empty image: {image_file}"
    encoded = base64.b64encode(raw).decode("ascii")
    text = text.replace(marker, f"data:{mime};base64,{encoded}")
assert not re.search(r"__IMAGE_ASSET_[A-Za-z0-9_]+__", text), "Unreplaced placeholder"
images = ET.fromstring(text).findall(".//{http://www.w3.org/2000/svg}image")
assert images, "No image elements found"
for image in images:
    keys = ("href", "{http://www.w3.org/1999/xlink}href")
    hrefs = [image.attrib[key] for key in keys if key in image.attrib]
    assert hrefs, "Image has no href"
    for href in hrefs:
        assert re.match(r"^data:image/[^;,]+;base64,", href), "External or invalid image reference"
        assert base64.b64decode(href.split(",", 1)[1], validate=True), "Empty image payload"
    assert image.get("preserveAspectRatio") == "xMidYMid meet", "Incorrect aspect ratio"
svg_file.write_text(text, encoding="utf-8")  # 全部校验通过后写入
print(f"Embedded and validated {len(images)} image(s): {svg_file}")
PY
```

交付前核对每个图片提示及 `asset_refs` 均已展示真实图片，SVG 可解析，所有图片引用均为有效内嵌数据；不得残留占位符、`../pictures/`、`../picture/` 等外部路径。图片提示不得作为正文渲染。实际预览检查图片完整、比例正确、图中文字及衬底清晰。
