# 风格七：牛津学院与复古科学图谱风（Oxford Collegiate & Monocle Infographics）

> 灵感源自 **牛津大学出版社（Oxford University Press）学术图谱、《Monocle》杂志信息图表（Infographics）与韦斯·安德森（Wes Anderson）对称学院美学**。采用极具辨识度的**双层画框装裱基底（青瓷灰绿外衬垫 + 暖象牙羊皮内画心 + 四角黄铜双线内框）**，结合**牛津深海军蓝（Oxford Navy）、学院绯红（Crimson Seal）、剑桥松石绿（Cambridge Teal）与芥末鎏金（Mustard Brass）**四大经典学院色，搭配**燕尾绶带（Swallowtail Ribbons）、学院盾徽（Collegiate Shields）、档案索引耳标（Index Tabs）与火漆印章**，打造出兼具严谨科学感、智性权威感与复古信息图美学的演示体验。

---

## 1. 色彩系统（Collegiate & Infographic Palette）

### 1.1 双层画框装裱基底（Double-Mat Framed Canvas）
- **外层装裱衬垫（Cambridge Celadon Mat）**：全画布 `1280×720` 填充柔和的剑桥青瓷灰绿 `#D6E2DC`（带极细斜纹或格纹肌理）。
- **内层羊皮画心（Warm Vellum Sheet）**：居中绘制 `x="24" y="20" width="1232" height="680" rx="18"` 的暖象牙画心 `#FAF6EE`，外围包裹 `2.5px` 牛津海军蓝 `#14213D` 实线框，并在内侧缩进 `6px` 处绘制 `1px` 芥末黄铜 `#C59B27` 装饰细框与四角花饰，一眼区别于所有无边框全屏画布风格。

### 1.2 核心学院四色（Core Collegiate Colors）
- **牛津深海军蓝（Oxford Navy）**：`#14213D`（主结构框线、核心焦点大卡底色、一级标题色）
- **哈佛学院绯红（Collegiate Crimson）**：`#B91C1C` / `#D9381E`（避坑警示印章、核心痛点高亮、燕尾红绶带）
- **剑桥松石青绿（Cambridge Teal）**：`#0F766E` / `#115E59`（科学方法论、正面示范、量化分级标尺）
- **芥末古典鎏金（Mustard Brass）**：`#D97706` / `#B45309`（时间节奏节点、星级勋章、内框铜线）

### 1.3 卡片与信息图表面（Card Surfaces）
- **经典象牙档案卡（Ivory Dossier Card）**：
  - 填充：`#FFFFFF`
  - 边框：`stroke="#14213D" stroke-width="2"`，底部叠加快速识别的 `4px` 厚书脊色带（`#14213D`、`#0F766E`、`#B91C1C` 或 `#D97706`）
- **牛津深蓝主焦点卡（Oxford Navy Hero Card）**：
  - 填充：`#14213D`，内嵌 `1px` `#C59B27`（透明度 `0.55`）金色内框线
  - 内部文字：主标题纯白 `#FFFFFF`，高亮文字使用鎏金黄 `#FCD34D` 或松石青 `#5EEAD4`，辅助文字 `#CBD5E1`
- **功能语义分色底卡**：
  - **绯红避坑卡（Crimson Pitfall Tint）**：填充 `#FEF2F2`，边框 `#B91C1C`
  - **松石科学卡（Teal Method Tint）**：填充 `#F0FDFA`，边框 `#0F766E`
  - **琥珀节奏卡（Amber Rhythm Tint）**：填充 `#FFFBEB`，边框 `#D97706`
  - **牛津浅蓝卡（Navy Tint）**：填充 `#EFF6FF`，边框 `#1E3A8A`

---

## 2. 字体与排版规范（Typography）

- **标题字体族（人文衬线与粗体无衬线混排）**：
  - 主标题与经典金句优先使用高识别度黑体/人文衬线：`'PingFang SC', 'Songti SC', 'Source Han Serif SC', 'Georgia', serif`
- **英文与数字图谱字体族（学院几何/衬线）**：
  - 章节编号、量化指标（如 `1000L`、`15%`、`ASQ`、`SEL`）：`'Georgia', 'Times New Roman', 'SF Pro Rounded', monospace`
- **字号层级标准**：
  - **封面主标题**：`48px - 56px`，`font-weight="900"`，深海军蓝 `#14213D`
  - **页面顶部主标题**：`28px - 32px`，`font-weight="800"`，置于顶部学院铭牌栏内
  - **卡片二级标题（`##`）**：`21px - 24px`，`font-weight="800"`
  - **正文与列表项**：`17px - 20px`，`font-weight="600"`（重点结论 `font-weight="800"`）
  - **档案编号与耳标**：`12px - 14px`，`font-weight="800"`，`letter-spacing="1.5"`

---

## 3. 标志性视觉组件（Signature Components）

### 3.1 学院盾徽与燕尾绶带（Collegiate Shield Crest & Swallowtail Ribbon）
- **牛津盾徽（Shield Crest）**：在封面、目录或章节主卡左上角绘制经典盾牌轮廓（`<path d="M 0 0 L 44 0 L 44 26 C 44 40 22 50 22 50 C 22 50 0 40 0 26 Z"/>`），内部印有罗马数字或章节编码（如 `I`、`II`、`01`）。
- **燕尾丝带标签（Swallowtail Ribbon）**：用带右侧三角燕尾缺口的多边形（`<polygon points="0,0 130,0 118,15 130,30 0,30"/>`）承载分类标签（如 `CHAPTER 01`、`CORE METHOD`、`PITFALL`）。

### 3.2 档案索引耳标卡（Index-Tabbed Dossier Cards）
- 每张 Bento 卡片顶部或左侧带有凸出的**彩色档案耳标（Folder Tab）**，底部配有 `4px` 实心学院色书脊底座，卡片内部采用 `1.5px` 实线与虚线（`stroke-dasharray="5 5"`）分割不同层级的条目，宛如精心排版的《Monocle》教育特辑图谱。

### 3.3 标尺刻度与火漆章（Infographic Ruler & Wax Stamp）
- 涉及年龄、年级、蓝思值（`10L -> 1000L`）或测评指标时，搭配可视化**学院刻度标尺（Ruler Ticks）**或**双环火漆印章（Double-Ring Stamp）**，强化科学量化感。

---

## 4. 页面类型设计范式（Slide Archetypes）

### 4.1 封面页（Cover）
- 双层青瓷/象牙画框内，左侧为大型**牛津学院铭牌主舞台**（带燕尾红金绶带、大号主标题与双线副标题框），右侧为一座**牛津深海军蓝科学教育图谱舱（Collegiate Atlas Panel）**，展示盾牌院徽、进阶阶梯与学科罗盘图形。

### 4.2 目录页（Table of Contents）
- 采用 **3×2 学院档案卡片矩阵（Collegiate Dossier Grid）**，每张卡片左上角悬挂一枚专属配色的**盾形院徽序号（`01` - `06`）**与燕尾小标签，首张卡片可采用牛津深海军蓝 `#14213D` 突出视觉重心。

### 4.3 正文内容页（Content Bento Grid）
- **顶部学院通栏铭牌（Top Collegiate Header Bar）**：左置盾形徽章与页面主标题，右置双线页码印章（`PAGE 03 / 13`）。
- **核心结论绶带横幅（Thesis Navy Banner）**：若页面含加粗核心论点（如“差距核心：并非纯粹靠大量时间堆积和低效内卷...”），将其置于顶部或底部的**牛津深海军蓝金边横幅卡**中，配以鎏金燕尾绶带。
- **对比与进阶矩阵**：误区/避坑内容采用**绯红印章卡**，科学方法/正面案例采用**松石绿或深海军蓝图谱卡**，时间节奏采用**琥珀金阶梯卡**，卡片间距保持 `>= 20px`。
