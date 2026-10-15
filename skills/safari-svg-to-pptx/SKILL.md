---
name: safari-svg-to-pptx
description: >-
  用 macOS Safari 打开 SVG 并截图，再把每张截图作为铺满全屏的图片写入已有 PowerPoint。
  输入可以是单个 .svg，或一个文件夹（只取该层全部 .svg，按文件名自然排序，一图一页）。
  当用户要求用 Safari 打开 SVG、截图插入 PPT、按空白页全屏图片模板灌页，或给出 svg 文件夹和 pptx 时使用。
---

# Safari SVG 截图写入 PPT

用本机 Safari 渲染 SVG，截取页面，写入已有 PPT 的全屏图片页。一图一页。不要改用 Chrome、WKWebView、rsvg、`screencapture` 或 computer use，也不要另写一套 WebDriver / OOXML。

## 命令

脚本在本 Skill 目录下：`scripts/svg_safari_to_pptx.py`（与本 `SKILL.md` 同级的 `scripts/`）。先定位本文件所在目录，再执行相对路径。不要写死 `~/.cursor/skills/...` 或任何安装位置，Skill 目录以后会换地方。

`--svg`、`--pptx`、`--output` 用用户给出的路径；相对路径相对于当前工作目录。

先核对顺序，再正式写入：

```bash
python3 scripts/svg_safari_to_pptx.py \
  --svg "page.svg 或 svg文件夹" \
  --pptx "deck.pptx" \
  --dry-run

python3 scripts/svg_safari_to_pptx.py \
  --svg "page.svg 或 svg文件夹" \
  --pptx "deck.pptx"
```

- `--svg` 可重复。文件按给定顺序；文件夹只取当前这一层的 `.svg` / `.SVG`，不进入子文件夹。
- 同一文件夹内按文件名自然排序：`page-2` 在 `page-10` 前，`page-001` 在 `page-002` 前。
- 默认覆盖 `--pptx` 指向的文件。用户要另存时加 `--output`。
- 截图同时保存到 PPT 同目录的 `safari-captures/`。

运行时会弹出一个自动化 Safari 窗口，结束后脚本会关掉它。不要对用户正在用的 Safari 执行「退出」。

## 页怎么对应

PPT 里要已有「铺满整页的图片占位」页（空白页模板：一张图盖住整个幻灯片）。没有这种页时脚本会失败，不要改去新建别的版式。

- 整份 PPT 都是这种全屏图片页：结果页数等于 SVG 张数。不够就克隆该空白页再追加；多出来的空白页删掉。
- PPT 里还有其他内容页：按文档顺序填入已有的全屏图片页，不够则在末尾按同一模板追加。不删除其他页，也不删多出来的空白页。

幻灯片宽高比以 `ppt/presentation.xml` 的 `p:sldSz` 为准。截图会铺满视口；若像素比例和幻灯片不一致，脚本按中心裁成相同比例再拉伸铺满，避免压变形。

## 已经处理过的特殊情况

这些情况脚本已经处理。遇到时重跑本脚本，不要改渲染器，也不要另写一套 OOXML。

- **全屏尺寸在版式上，不在幻灯片上。** 空白页往往只有一个 `type="pic"` 占位，`<p:spPr/>` 是空的，位置在所引用的 `slideLayout` 里。`--dry-run` 若因此报「没有铺满全屏的图片页」，先确认占位是否继承版式尺寸，不要当成缺少模板去新建版式。版式关系的 `Target`（如 `../slideLayouts/slideLayout1.xml`）相对于幻灯片部件目录 `ppt/slides/`，不是 `_rels` 目录。
- **导航先停在空白页。** WebDriver 使用 `pageLoadStrategy: none`。打开 SVG 后要等到文档是 `svg` 且 `readyState` 为 `complete` 再截图；刚返回时经常还是 `about:blank`。
- **本机代理会拦住本机地址。** 环境里若有 `http_proxy`，访问 `127.0.0.1` 可能得到 502。WebDriver 和本地预览必须绕过代理。不要用 `file://` 打开 SVG，自动化 Safari 下会一直不返回。
- **自动化窗口中途被关掉。** 报错含 `no such window`，或单页脚本超时。脚本会重新打开自动化 Safari，并只重试当前这一页，最多 2 次。请用户不要关掉弹出的那个窗口。不要因此退出用户正在用的 Safari。

## 失败时

退出码 `2`：Safari 还不能被 WebDriver 控制。请用户任选一种方式打开后再重跑同一条命令，不要代输密码：

1. 在「终端」执行 `safaridriver --enable`，输入开机密码。
2. Safari → 设置 → 开发者 → 勾选「允许远程自动化」。没有「开发者」时，先在「设置 → 高级」打开「在菜单栏中显示开发菜单」。

其他失败：把脚本的报错原文告诉用户，不要改用别的渲染器重做。

## 做完之后

用用户的语言说明写入了哪份 PPT、共几页、文件名顺序。不要复述脚本内部端口或会话 id。
