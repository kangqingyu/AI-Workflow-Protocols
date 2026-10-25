# 风格六：VisionOS 极光珠光全息玻璃风（VisionOS Iridescent Pearl & Holographic Prism）

> 灵感源自 **Apple VisionOS 空间计算界面、WWDC 设计大奖（Apple Design Awards）与珠光全息光学棱镜（Iridescent Pearl & Holographic Glass）**。摒弃厚重的暗黑背景或粗野硬边，以**高明度珠光极光画布（Luminous Pearl & Spatial Aurora Mesh）**为基底，融合**双层高光折射磨砂玻璃卡（Specular Pearl Glass）**、**深空全息棱镜主卡（Deep Cosmos Holographic Card）**与**iOS 超椭圆流光应用徽章（Squircle App Icon Badges）**，呈现出兼具未来空间感、通透光学质感与苹果生态旗舰发布会的视觉体验。

---

## 1. 色彩系统（Iridescent Pearl & Holographic Palette）

### 1.1 画布与极光流体基底（Spatial Canvas）
- **珠光漫反射基底（Pearl Base Gradient）**：`135deg` 线性渐变，从冷调珍珠白 `#EEF2FF` 过渡至极光淡紫 `#F5F3FF` 与冰川浅青 `#ECFEFF`。
- **空间极光光球（Aurora Mesh Orbs）**：使用径向渐变（`radialGradient`）在背景层叠加 3 个柔和弥散的极光光斑：
  - 左上/中上：**全息紫粉光晕**（`#A855F7` → `#EC4899`，中心透明度 `0.18` 渐变至 `0`）
  - 右下：**App Store 冰蓝光晕**（`#0EA5E9` → `#6366F1`，中心透明度 `0.18` 渐变至 `0`）
  - 左下/右侧：**暖珊瑚金光晕**（`#F97316` → `#F43F5E`，中心透明度 `0.12` 渐变至 `0`）
- **空间同心光轨（Spatial Orbit Rings）**：画布背景绘制极细的纯白高光环（`stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="1.5"`）与淡靛蓝光学刻度环（`stroke="#6366F1" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="6 8"`），营造 VisionOS 空间景深。

### 1.2 空间玻璃与全息卡片色板（Spatial Glass Surfaces）
- **珠光高透磨砂主卡（Frosted Pearl Glass）**：
  - 填充：`linearGradient (0,0 -> 0,1)` 从 `#FFFFFF` (`opacity="0.94"`) 到 `#F8FAFC` (`opacity="0.82"`)
  - 外框高光折射边（Specular Rim）：`stroke="url(#pearlRimGrad)" stroke-width="2"`（左上纯白 `#FFFFFF` → 中部淡紫蓝 `#C7D2FE` → 右下淡青 `#BAE6FD`）
  - 顶部高光弧线：卡片内侧顶部 `1.5px` 纯白亮线，模拟空间玻璃边缘折射。
- **深空全息棱镜焦点卡（Deep Cosmos Holographic Hero Card）**：
  - 填充：`linearGradient (0,0 -> 1,1)` 从深空靛黑 `#0F172A` → 皇家暗紫 `#1E1B4B` → 极夜星云 `#2E1065`
  - 外框全息流光边：`stroke="url(#holoRimGrad)" stroke-width="2"`（`#38BDF8` → `#A855F7` → `#F472B6`）
  - 内部文字：主标题纯白 `#FFFFFF`，高光强调色使用全息冰蓝 `#38BDF8`、极光粉 `#F472B6` 或星芒金 `#FBBF24`，辅助正文 `#CBD5E1`。
- **极光炫彩玻璃分卡（Tinted Prism Glass Cards）**：
  - **App Store 蔚蓝玻璃（Azure Glass）**：填充 `#F0F7FF` → `#E0E7FF`（透明度 `0.88`），边框 `#BFDBFE`，主题渐变 `#0066FF` → `#06B6D4`
  - **WWDC 霓虹紫粉玻璃（Amethyst Rose Glass）**：填充 `#FAF5FF` → `#FCE7F3`（透明度 `0.88`），边框 `#E9D5FF`，主题渐变 `#7C3AED` → `#EC4899`
  - **翡翠青柠玻璃（Emerald Mint Glass）**：填充 `#ECFDF5` → `#CCFBF1`（透明度 `0.88`），边框 `#A7F3D0`，主题渐变 `#059669` → `#0D9488`
  - **落日珊瑚玻璃（Sunset Coral Glass）**：填充 `#FFF7ED` → `#FFE4E6`（透明度 `0.88`），边框 `#FED7AA`，主题渐变 `#EA580C` → `#E11D48`

### 1.3 文字色彩层级（Typography Hierarchy）
- **珠光浅色卡文字**：
  - 一级标题 / 核心结论：深空钛黑 `#0F172A`
  - 二级小标题：深邃靛蓝 `#1E1B4B`
  - 正文主色：高对比石板灰 `#334155`
  - 次要信息 / 标签注脚：冷调中性灰 `#64748B`
- **深空全息卡文字**：
  - 一级标题 / 核心数字：纯白 `#FFFFFF`
  - 强调高亮：全息青 `#38BDF8` / 极光粉 `#F472B6` / 琥珀金 `#FBBF24`
  - 正文说明：星云银灰 `#E2E8F0`

---

## 2. 字体与排版规范（Typography）

- **主字体族（现代苹果无衬线）**：
  `font-family="'SF Pro Display', 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"`
- **数字与代码字体族（几何等宽/圆体数字）**：
  `font-family="'SF Pro Rounded', 'SF Mono', 'JetBrains Mono', 'PingFang SC', monospace"`
- **字号与字重标准**：
  - **封面主标题**：`50px - 58px`，`font-weight="800"`，字距紧致，可搭配深空或极光渐变装饰条
  - **封面副标题**：`22px - 26px`，`font-weight="500"`，置于高透磨砂胶囊或全息铭牌内
  - **内容页主标题（悬浮顶栏）**：`30px - 34px`，`font-weight="800"`，颜色 `#0F172A`
  - **卡片二级标题（`##`）**：`20px - 23px`，`font-weight="700"`
  - **卡片正文与列表项**：`16px - 19px`，`font-weight="500"`（关键句 `font-weight="700"`）
  - **空间胶囊角标 / 序号徽章**：`13px - 15px`，`font-weight="700"`，`letter-spacing="1.2"`

---

## 3. 标志性视觉组件（Signature Components）

### 3.1 VisionOS 悬浮空间胶囊顶栏（Spatial Floating Top Bar）
- 内容页顶部不采用通栏死板色块，而在左上角只展示单行页面主标题 `pages[0].title`（左侧可搭配一枚纯图形流光圆点或超椭圆图标，**严禁在主标题上方或左侧额外输出一行 `part_title` 小字胶囊**，避免标题重复）；右上角 `x="1080" y="34"` 放置一枚**空间控制胶囊（Spatial Window Pill）**，内置三枚微光光学圆点与当前页码 `01 / 25`。

### 3.2 iOS 超椭圆流光应用图标徽章（Squircle App Icon Badges）
- 卡片左上角或标题旁配备标志性的 **iOS App Icon 超椭圆徽章**（尺寸 `40x40` 至 `56x56`，圆角 `rx="12"` 至 `rx="16"`）：
  - 底层为高饱和苹果生态多段渐变（如 App Store 蓝 `#0066FF -> #00C6FF`、TestFlight 青紫 `#4F46E5 -> #06B6D4`、Apple Design 玫瑰紫 `#9333EA -> #F43F5E`）；
  - 上半部叠加一层半透明白色弧形高光罩（`fill="#FFFFFF" fill-opacity="0.22"`），还原 iOS 图标的玻璃光泽；
  - 内部居中绘制纯白矢量图标或序号。

### 3.3 双层折射 Bento 卡片与内嵌微胶囊（Dual-Layer Specular Bento Cards）
- **大圆角空间曲面**：主卡片统一使用 `rx="26"` 或 `rx="28"`，子卡片/内嵌行使用 `rx="16"` 或 `rx="18"`。
- **柔和空间悬浮阴影**：通过 `<filter id="spatialShadow">`（`feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#1E1B4B" flood-opacity="0.08"`）赋予卡片轻盈的空气悬浮感，绝不使用生硬黑边。
- **内嵌高光微胶囊（Inner Glass Sub-Pills）**：当卡片内包含多个要点（`- `）时，可将每条要点装入独立的内嵌半透明微胶囊（`fill="#FFFFFF" fill-opacity="0.78" stroke="#E2E8F0" stroke-width="1.2" rx="14"`），左侧搭配渐变圆点或胶囊标签，让长文本结构清晰、呼吸感十足。

---

## 4. 页面类型设计范式（Slide Archetypes）

### 4.1 封面页（Cover）
- **空间极光舞台**：画布中央偏左构建一块超大尺寸的**珠光高透空间主面板（Spatial Hero Glass Window，`rx="36"`）**，右侧或环绕位置悬浮 **3 枚立体 iOS App Icon 超椭圆全息徽章 / 深空棱镜数据卡**，呈现层次丰富的空间计算景深。
- **底部全息信息坞（Spatial Dock）**：底部居中或左对齐放置一条模仿 VisionOS / macOS Dock 的高透毛玻璃托盘，承载副标题或核心标签。

### 4.2 目录页（Table of Contents）
- 采用 **2×3 或 3×2 空间应用矩阵（App Matrix Bento Grid）**。每个章节宛如一枚独立的 VisionOS 空间应用卡片：左上角配有专属渐变色的 **iOS Squircle 序号图标（`01` - `06`）**，卡片底部带有极光渐变进度细线；其中重点章节或首章可采用深空全息紫蓝渐变高亮。

### 4.3 里程碑 / 核心金句页（Milestone / Hero Statement）
- 当某页正文仅有单句重磅陈述（如“2025年，上架了5款App”）时，切勿留白空洞：
  - 中央打造一座**深空全息棱镜巨幕卡（Deep Cosmos Holographic Stage）**承载核心大字与发光数字；
  - 环绕或下方排列 **5 枚极具视觉冲击力的 iOS 超椭圆流光 App 图标阵列（01–05 Squircle Dock）**，用纯视觉图形语言呼应核心主题（严格不添加 JSON 以外的额外解释文字）。

### 4.4 正文内容页（Content Bento Grid）
- **核心结论横幅（Thesis Prism Banner）**：若页面首段存在加粗核心结论（`**...**`），将其置于顶部通栏的**深空全息横幅卡**或**极光渐变高光胶囊**中，一眼抓住视觉重心。
- **多维 Bento 矩阵**：根据 `##` 二级标题数量（2 栏、3 栏、上 1 下 2、左 1 右 2 等）动态排布珠光玻璃卡，每张卡片赋予不同色相的 iOS Squircle 徽章与顶部极光折射饰条，确保卡片间距 `>= 22px`，四周留白充裕。
