---
name: single-json-to-guizang-ppt
description: >-
  根据文章原稿（.md）与 JSON 大纲目录（*-json-outline/），组合调用 guizang-ppt-skill
  生成横向翻页单文件网页 PPT（含 WebGL 背景、双屏演讲者模式、逐字稿备注、CleanShot X 风格配图合成及自动化校验）。
  当用户提供文章原稿与 json-outline 文件夹并要求生成网页 PPT 时使用。
---

# 文章原稿 + JSON 大纲 → 归藏网页 PPT (`json-to-guizang-ppt`)

本 Skill 是 [article-to-ppt20261006](file:///Users/kqy/.gemini/config/skills/article-to-ppt20261006/SKILL.md) 的下游网页 PPT 渲染器，通过**组合调用**底层 [guizang-ppt-skill](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/SKILL.md) 的模板、背景资产与校验脚本，将「文章原稿 + 逐页 JSON 大纲」转化为可双屏演讲的单文件网页 PPT。

---

## Step 0：读取底层 `guizang-ppt-skill` 规范与模板

在开始生成前，**必须按需读取**底层 `guizang-ppt-skill` 的规范与模板文件：

1. 主规范：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/SKILL.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/SKILL.md)
2. 模板基座：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/template.html](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/template.html)（若用户指定瑞士风则使用 `assets/template-swiss.html`）
3. 布局与主题参考：
   - 页面布局库：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/layouts.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/layouts.md)
   - 主题色板：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/themes.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/themes.md)
   - 截图画框规范：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/screenshot-framing.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/screenshot-framing.md)
   - 双屏演讲者模式规范：[/Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/presenter-mode.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/presenter-mode.md)

---

## Step 1：解析输入契约（Input Resolution）

支持以下输入形式（若用户只提供其中一项，自动在同级目录推导其余路径）：

1. **文章原稿（`.md`）**：例如 `<文章名>.md`，用于提取完整上下文、生动案例、数据细节及演讲逐字稿（`speakerNotes`）。
2. **JSON 大纲目录（`*-json-outline/`）**：包含：
   - `page-001.json` ~ `page-NNN.json`：每一页 PPT 的结构化节点（`title`、`sub_title`、`content` 树）。
   - `outline.txt`：章节大纲与页面索引总览。
   - `outline-info.json`（可选）：包含每页附加的 `images` 与 `remarks` 提示。
3. **原稿配图目录（`pictures/` 或同级图片）**：自动检索原稿或 JSON 中 `图片（使用附件中图片：xxx）` / `> 如图：xxx` 所引用的本地图片文件。

---

## Step 2：默认偏好与免打扰策略（Default Preferences）

除非用户在 Prompt 中明确指定其他视觉风格，或主动要求“先向我提问确认”，否则**默认采用以下配置直接生成**，无需弹窗打断用户：

| 配置维度 | 默认策略（可通过用户 Prompt 覆盖） |
| :--- | :--- |
| **视觉风格与配色** | **风格 A：电子杂志 × 电子墨水（🖋 墨水经典）** — 暖米白纸底 `#f1efea` + 纯墨黑 `#0a0a0b` + WebGL 流体 Shader 背景 |
| **页数与结构映射** | **严格 1:1 映射**：总页数严格等于 `page-001.json` ~ `page-NNN.json` 的文件总数，按页码顺序一一对应 |
| **占位符标题润色** | 遇到 `"title": "todo ..."` 或空标题时，结合 `文章原稿.md` 对应章节核心观点，提炼正式简短的主标题（≤ 20 字）与英文/中文 `kicker` |
| **章节提问引入页** | 遇到 `"# Q"` 或提问式章节页，渲染为 `hero dark` 或 `hero light` **幕封问题页（Hero Question / Act Divider）**，营造章节呼吸节奏 |
| **原稿配图处理** | 自动定位 JSON 中引用的本地图片，使用 [frame_image.swift](file:///Users/kqy/.gemini/config/skills/json-to-guizang-ppt/scripts/frame_image.swift) 搭配内置背景 `monocle-classic.webp` 合成 `16:10`（1600×1000）CleanShot X 圆角阴影画框图，输出至 `ppt/images/` |

---

## Step 3：逐页内容映射与版式编排规范

遍历 `page-001.json` 至最后一页，结合 `文章原稿.md` 完成高信息密度、视觉多样化的版式设计：

1. **严格遵守 [layouts.md](file:///Users/kqy/.gemini/config/skills/guizang-ppt-skill/references/layouts.md) 类名与节奏规范**：
   - 只使用 `template.html` 预定义的标准类（`h-hero`、`h-xl`、`h-sub`、`h-md`、`lead`、`meta-row`、`stat-card`、`pipeline`、`step`、`grid-2-7-5`、`grid-2-6-6`、`grid-2-8-4`、`grid-3`、`grid-4`、`grid-6`、`frame-img`、`callout`、`kicker` 等）。
   - **Hero 与 Non-Hero 交替节奏**：`hero` 页（封面、章节幕封、核心提问页、收尾页，透出 WebGL 流体背景）与 `non-hero` 正文页按约 `1 : 2~3` 交错，避免连续超过 3 页完全相同的布局。
   - **图文页（含本地配图）**：单图采用 `.grid-2-7-5` 或 `.grid-2-6-6` 搭配 `.frame-img.r-16x10`；双图并列采用 `.grid-2-6-6` 搭配同高 `.frame-img.r-16x10`。
2. **文案精炼铁律（Slide Copy）**：
   - 幻灯片画面遵循“一页一核心观点”，卡片正文简明扼要，善用对比色块、数字提取（Stat Card）与步骤流（Pipeline）。
   - 详细故事、人物案例、实验数据下沉到 `speakerNotes` 演讲逐字稿中。
3. **演讲者逐字稿（`speakerNotes`）**：
   - 在 `index.html` 底部脚本的 `speakerNotes` 数组中，为每一页提供与 `<section id="sNN">` 严格对应的 `{ id, title, minutes, notes }`。
   - `notes` 需紧密还原 `文章原稿.md` 中的金句、故事案例与推导逻辑，口语化自然流畅，让演讲者打开 `P` 键演讲者控制台即可直接照念。

---

## Step 4：配图合成与离线依赖准备

1. **创建输出目录并复制模板与离线动画库**：
   ```bash
   mkdir -p "<文章目录>/ppt/images" "<文章目录>/ppt/assets"
   cp /Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/motion.min.js "<文章目录>/ppt/assets/motion.min.js"
   cp /Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/template.html "<文章目录>/ppt/index.html"
   ```
2. **合成 CleanShot X 风格 `16:10` 配图**：
   先将内置主题背景转换为临时 PNG，再调用本 Skill 自带的原生 Swift 脚本 [frame_image.swift](file:///Users/kqy/.gemini/config/skills/json-to-guizang-ppt/scripts/frame_image.swift)（使用 macOS 原生 `AppKit`，零第三方依赖）：
   ```bash
   ffmpeg -y -i /Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/screenshot-backgrounds/style-a/monocle-classic.webp /tmp/monocle-bg.png 2>/dev/null
   swift -module-cache-path /tmp/swift-module-cache \
     /Users/kqy/.gemini/config/skills/json-to-guizang-ppt/scripts/frame_image.swift \
     /tmp/monocle-bg.png \
     "<原稿图片路径>" \
     "<文章目录>/ppt/images/<页码>-<语义名>.jpg" \
     18 0.08 0
   ```

---

## Step 5：输出产物与自动化校验（Mandatory Validation）

1. **生成文件清单**：
   - `<文章目录>/ppt/index.html`：完整单文件网页 PPT。
   - `<文章目录>/ppt/assets/motion.min.js`：本地 Motion One 动画库兜底。
   - `<文章目录>/ppt/images/*.jpg`：合成后的 `16:10` CleanShot X 风格配图。
   - `<文章目录>/ppt/项目记录.md`：包含视觉规格、页码与 `page-XXX.json` 1:1 映射表、配图清单及快捷键说明。
2. **运行强制校验脚本**：
   生成完毕后，**必须运行** `guizang-ppt-skill` 的校验脚本验证双屏同步协议与逐字稿完整性：
   ```bash
   node /Users/kqy/.gemini/config/skills/guizang-ppt-skill/scripts/validate-presenter-mode.mjs "<文章目录>/ppt/index.html"
   ```
   - 必须确保输出 `0 errors, 0 warnings`，且检测到的 `slides` 数量与 `*-json-outline/page-*.json` 数量严格一致。
