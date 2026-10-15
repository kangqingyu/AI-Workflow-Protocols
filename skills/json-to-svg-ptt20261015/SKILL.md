---
name: json-to-svg-ptt20261015
description: 根据json大纲，输出svg格式PPT演示文稿





---


作为精通信息架构与 SVG 编码的专家，你的任务是将完整的文字内容转化为一张高质量、结构化、具备高级感、简洁感和专业感的 SVG 演示文稿页面。要求如下：

1.画布: SVG viewBox 必须是 0 0 1280 720。

2.内容页的便当网格 (Bento Grid) 布局
这是一种灵活的网格系统，其布局应由内容本身的需求驱动，而非僵硬的模板。通过组合不同尺寸的卡片，创造出动态且视觉有趣的布局。
- 核心原则:
    - 灵活性: 卡片数量不固定。可以是 1, 2, 3, 4, 5 或更多个，取决于如何更好地呈现信息。
    - 层级感: 使用卡片尺寸建立视觉层级。最重要的信息放在最大的卡片上。
    - 留白: 在所有卡片之间保持至少 20px 的间距。
- 布局组合示例:
    - 单一焦点: 一张大卡片覆盖大部分区域 (w=1200, h=580)。适用于单一、有力的信息或详细的图表。
    - 两栏布局:
        - 50/50 对称: 两张等宽的卡片。
        - 非对称: 一张较宽的卡片（如 2/3 宽度）用于主内容，一张较窄的（1/3 宽度）用于辅助信息、数据或图片。
    - 三栏布局: 三张等宽的卡片，适合并列比较三项内容。
    - 主次结合: 一张大的居中卡片，两侧各一张小的垂直卡片。
    - 顶部英雄式: 顶部一张宽幅“英雄”卡片，下方是 2-4 个较小的等宽卡片网格。
    - 混合网格 (自由度最高): 自由混合各种尺寸的卡片，例如一个中等方块、两个小的水平矩形和一个垂直矩形。这种方式可以极大地适应不同内容的需求。



## SVG中文字要求
根据json结构，保持和json中一样的文字，避免添加过多解释性文字。

## 图片处理与防引用失败规范（强制执行）
当 JSON 内容中出现图片提示（如 `图片（使用附件中图片：xxx）`）或 `outline-info.json` 中该页存在 `asset_refs` 时，**必须使用原文真实图片，严禁手绘替代或仅留空白/文字占位，且严禁在最终 SVG 中保留外部相对/绝对文件路径**：

1. **精准定位与存在性校验**：
   - 查阅同目录下的 `outline-info.json`，通过当前页的 `asset_refs` 匹配顶层 `assets` 列表，获取图片的 `path` 与 `original_reference`。
   - **必须校验文件实际存在**：在终端或通过工具确认图片文件真实路径（注意排查文件名空格差异，如 `pictures/` 或 `picture/`、`assets/` 目录）。
2. **强制使用 Base64 Data URI 内嵌（杜绝路径失效与预览拦截）**：
   - macOS QuickLook（空格预览）、IDE 预览器及浏览器沙箱会拦截 SVG 中的外部本地路径（如 `href="../pictures/xxx.png"`），且目录层级变动会导致相对路径失效。
   - **所有引用的图片必须转换为 `data:image/<ext>;base64,...` 格式直接内嵌到 `<image>` 标签中**。
   - `<svg>` 根节点需声明 `xmlns:xlink="http://www.w3.org/1999/xlink"`，`<image>` 标签需设置 `preserveAspectRatio="xMidYMid meet"`（如原图为白底图表，建议为其容器设置浅色/白色内衬底板 `#ffffff` 与圆角 `clipPath`，确保在深色主题下清晰可读）。
3. **高效内嵌执行方式（避免大模型直接手写截断 Base64）**：
   - 先生成结构完整的 SVG 文件（可在 `<image>` 的 `href` 中先写占位符如 `__IMAGE_ASSET_1__` 或相对路径）。
   - 紧接着使用 Python 脚本读取真实图片文件并替换为完整的 Base64 Data URI，并校验替换结果：
     ```bash
     python3 -c '
     import base64, mimetypes, pathlib
     svg_file = pathlib.Path("path/to/page-XXX.svg")
     img_file = pathlib.Path("path/to/actual_image.png")
     assert img_file.is_file(), f"Image not found: {img_file}"
     mime = mimetypes.guess_type(img_file.name)[0] or "image/png"
     b64 = base64.b64encode(img_file.read_bytes()).decode("ascii")
     data_uri = f"data:{mime};base64,{b64}"
     text = svg_file.read_text(encoding="utf-8")
     # 将相对路径或占位符替换为 Base64 Data URI
     text = text.replace("__IMAGE_ASSET_1__", data_uri)
     svg_file.write_text(text, encoding="utf-8")
     assert "data:image/" in svg_file.read_text(encoding="utf-8"), "Base64 embed failed!"
     '
     ```
4. **交付前自检**：
   - 检查生成的 `.svg` 文件中是否包含 `data:image/`，确保没有任何残留的 `../pictures/`、`../picture/` 或未替换的占位符。
   - 确保 JSON 中形如 `图片（使用附件中图片：xxx）` 的提示指令已被转化为真实内嵌图片展示，不要将该提示指令当作普通正文渲染在画面上。

## 输出格式
1. 页数要求：每一个 JSON 文件，单独输出一页 `.svg` 代码文件。