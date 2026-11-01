# 风格十一：HHKB 极客机械键帽 × macOS 效率启动器工作台风（HHKB Tactile Keycap & macOS Power-User Workbench）

## 1. 风格定位与美学灵感

- **核心气质**：客制化静电容键帽触感（HHKB PBT Keycap Tactility）、macOS 极客命令启动器（Alfred / Raycast Command Bar）、节点自动化工作流（Keyboard Maestro Macro Pipeline）、硬核软件实验室横评（Software Benchmark Lab）。
- **设计灵感**：
  - **HHKB Professional（Happy Hacking Keyboard）经典白灰与炭黑墨刻键帽**：温润细腻的复古鹅卵石暖白（Pebble Ivory `#F4F2ED`）与浅灰修饰键（Modifier Warm Gray `#E5E2DC`），点缀定制 ESC 朱砂橙红键帽（`#E04F33`）与 Control/Option 皇家蓝键帽（`#2563EB`），带有微妙的立体键帽内凹高光与底部键座阴影。
  - **Alfred / Raycast / Keyboard Maestro / Karabiner 极客工作流界面**：悬浮式全局命令搜索框（Command Launcher Bar）、物理快捷键徽章（`⌥ Space`、`⌘ Space`、`⌃⌘ A`）、多步延迟执行脚本卡片（`Step 1 → Delay → Step 2`）。
  - **CleanShot X 与 Mac 开发者评测图谱**：高信息密度的软件对比评测卡（带记忆进度/倍速层级/传歌方式参数标签），一眼看清每款软件的真实体验优劣。
- **适用场景**：效率工具与软件评测、macOS/Windows 极客工作流、快捷键与外设定制（HHKB/Karabiner）、自动化脚本（Keyboard Maestro/AHK）、开发者工具链分享。

---

## 2. 色彩系统（HHKB 暖白键帽 × 炭黑命令栏 × Alfred 电光紫 × ESC 朱砂橙 × 极客翡翠绿）

| 角色 | 颜色名称 | Hex / 渐变建议 | 用途说明 |
|---|---|---|---|
| **画布主背景** | HHKB 经典鹅卵石暖灰白 | `#F4F2ED` → `#ECEAE4` → `#F2F0EB` | 1280×720 画布基底，还原高级 PBT 磨砂键帽与极客桌面质感 |
| **深色中枢卡底** | HHKB 炭黑墨色 / 命令栏深灰 | `#181C23` → `#222731` | 封面右侧命令终端、Alfred 启动栏、核心法则暗色卡片 |
| **普通卡片基底** | 纯白 PBT 键帽面 | `#FFFFFF`（配 `#DDD9D0` 外框与底部立体键帽投影） | Bento 卡片主体，模拟微立体悬浮键帽或 macOS 原生窗口 |
| **次级卡片基底** | 修饰键暖灰 | `#F5F3EE` / `#EAE7E0` | 快捷键槽、软件评测参数格、脚本步骤槽底色 |
| **主标题/正文墨色** | 热升华深炭黑 | `#14181F` | H1、H2、卡片主标题、核心结论文字 |
| **常规正文色** | 机械轴体石板灰 | `#333B48` | 正文列表、软件优缺点评测说明 |
| **次要元数据色** | 键帽侧刻冷灰 | `#68707E` | 页码、键位坐标（`ROW 1 // KEY 01`）、辅助标签 |
| **主强调色 A（启动器/自动化）** | Alfred 电光紫 | `#5B45FF`（浅底色 `#F0EEFF`） | Alfred 搜索、Keyboard Maestro 脚本、Workflow 自动化 |
| **主强调色 B（核心矛盾/ESC键）** | HHKB ESC 朱砂红橙 | `#E04F33`（浅底色 `#FDF0ED`） | 主要矛盾、真实痛点瓶颈、关键快捷键高亮 |
| **主强调色 C（通过/备份/微观）** | 极客终端翡翠绿 | `#0D9488`（浅底色 `#E6F7F5`） | 评测达标特性、云端+硬盘双保险、微观路线优化 |
| **主强调色 D（音视频/专业工具）** | 媒体控制琥珀蓝 | `#1D63DC` / `#D97706` | 音视频播放器倍速/字幕评测、macOS 专业开发与截图工具 |

---

## 3. 排版与字体规范

- **几何无衬线标题体（Tactile UI Sans）**：
  - `font-family: 'PingFang SC', 'SF Pro Display', 'Hiragino Sans GB', 'Microsoft YaHei', system-ui, sans-serif`
  - 用于：封面大标题、每页单行主标题、Bento 卡片标题（H2/H3）。
- **高清晰正文体（Benchmark Body）**：
  - `font-family: 'PingFang SC', 'SF Pro Text', 'Hiragino Sans GB', system-ui, sans-serif`
  - 用于：软件评测要点、操作步骤列表。
- **键帽热升华等宽体（Keycap Legend Monospace）**：
  - `font-family: 'JetBrains Mono', 'SF Mono', 'Menlo', monospace`
  - 用于：立体键帽字符（`Opt ⌥`、`Cmd ⌘`、`Ctrl ⌃`、`Space`）、倍速参数（`1.25x` / `1.5x` / `2.0x` / `+15s`）、页码（`01 / 21`）。

---

## 4. 标志性视觉组件（Signature Components）

### 4.1 立体 PBT 机械键帽徽章（3D Tactile Keycap Badge）
- 用双层圆角矩形模拟真实 HHKB 键帽：外层键座（`rx="10"`, 填充 `#D8D4CA` 或 `#C8C3B8`），内层键帽顶面向上偏移 `2px–3px`（`rx="8"`, 填充 `#FFFFFF`、`#E04F33` 或 `#5B45FF`），左上角刻印等宽热升华字符（如 `ESC`、`⌥ Opt`、`⌘ Cmd`、`FN`）。

### 4.2 Alfred / Raycast 悬浮命令启动栏（Floating Command Launcher Bar）
- 在封面、目录或效率工具页，使用带放大镜/快捷键提示的暗色或亮色圆角搜索栏组件（`⌘ + Space / ⌥ + Space`），直观传达“高频操作一键直达”的极客效率感。

### 4.3 软件实验室评测矩阵卡（Software Benchmark Matrix Card）
- 在多款软件对比页（如 12 款音频播放器横评、截图软件对比），每张卡片顶部带有软件名称与立体键帽编号，内部提炼可视化的属性胶囊（如 `记忆进度`、`倍速层级`、`快进10s/15s`、`Wi-Fi传歌`），再完整呈现原文评测结论。

### 4.4 单行主标题顶栏（Single-Line Keycap Header）
- 正文页左上角**只渲染单行页面主标题（`pages[0].title`）**，左侧搭配一枚精致的立体键帽色标；**严禁在主标题上方再输出一行 `part_title` 小字**（彻底杜绝“第一行小字、第二行大字”的重复标题）。目录页同理，`目录` 全页只出现一次。

---

## 5. 页面布局与核心红线

1. **画布尺寸固定**：`viewBox="0 0 1280 720" width="1280" height="720"`。
2. **文字完整性**：严格保留 JSON 大纲中的全部正文文字与层级结构，不遗漏任何要点，也不凭空编造大纲外的解释文字。
3. **Bento 网格间距**：卡片间距不少于 `20px`，四周安全边距不少于 `48px`（推荐左右边距 `56px`）。
4. **真实图片内嵌**：遇到 `图片（使用附件中图片：xxx）` 或 `asset_refs` 时，将其转化为带**极客桌面外设画框**的真实 Base64 Data URI `<image>`，不把图片提示语当作正文输出。
