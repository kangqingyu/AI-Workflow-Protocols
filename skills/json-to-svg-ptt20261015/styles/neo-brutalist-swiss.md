# 风格五：新粗野主义瑞士波普风（Neo-Brutalist Swiss Kinetic Grid）

灵感源自 **Figma Config 发布会视觉、Gumroad 设计系统、瑞士国际主义网格与新粗野主义（Neubrutalism）数字波普美学**。
与前四种风格（暗黑毛玻璃、圆角粘土色块、银灰工业硬件、古典暖纸书卷）完全区隔：本风格以**3px 纯黑硬朗描边（`#141416`）、45° 斜向实体硬阴影（`dx="+7" dy="+7"` 纯黑色块，绝不使用高斯模糊阴影）、桌面 OS 窗口顶栏（三色几何圆点 + 粗黑分割线）与高能电光波普色块（电光紫、酸性荧光绿、波普珊瑚红、赛博青、纯粹白、终端炭黑）**为核心视觉语言，极具数字原生张力与现代先锋设计感。

---

## 一、画布基底与粗野主义外框

1. **画布尺寸**：固定 `viewBox="0 0 1280 720" width="100%" height="100%"`。
2. **建筑坐标纸底板**：
   - 底色采用温润冷灰米白（`#F4F2EC` → `#EAE6DC`），铺设 `32×32` 瑞士工程方格网（`#D6D0C4`，`stroke-width="1"`）。
   - 画布四周绘制 `3px` 纯黑粗野主义主外框（`x="20" y="20" width="1240" height="680" rx="14" stroke="#141416" stroke-width="3"`），四角点缀十字准星或粗黑几何锚点。

```xml
<defs>
  <linearGradient id="brutalCanvasGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#F5F3EE" />
    <stop offset="100%" stop-color="#EAE6DC" />
  </linearGradient>
  <linearGradient id="violetBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#7047EB" />
    <stop offset="100%" stop-color="#5423E7" />
  </linearGradient>
  <linearGradient id="limeBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#D8FF29" />
    <stop offset="100%" stop-color="#BEEF00" />
  </linearGradient>
  <linearGradient id="coralBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#FF5470" />
    <stop offset="100%" stop-color="#E62E4D" />
  </linearGradient>
  <linearGradient id="cyanBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#38E5FF" />
    <stop offset="100%" stop-color="#00B8D9" />
  </linearGradient>
  <linearGradient id="amberBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#FFD83D" />
    <stop offset="100%" stop-color="#FFBE0B" />
  </linearGradient>
  <linearGradient id="carbonBrutalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#222226" />
    <stop offset="100%" stop-color="#141416" />
  </linearGradient>
  <pattern id="swissGrid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#D6D0C4" stroke-width="0.9" />
  </pattern>
</defs>

<rect width="1280" height="720" fill="url(#brutalCanvasGrad)" />
<rect width="1280" height="720" fill="url(#swissGrid)" />
<rect x="20" y="20" width="1240" height="680" rx="14" fill="none" stroke="#141416" stroke-width="3" />
```

---

## 二、色彩矩阵与高对比度规范

本风格通过**黑色粗描边（`3px`）+ 斜向实体黑影（`+7px, +7px`）**统一所有色块，每页从以下 6 种波普材质中取 3～4 种组合：

| 材质名称 | 表面填充 | 文字主色 | 强调文字 / 贴纸色 | 适用模块 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 纯白工作室板（Studio White）** | `#FFFFFF` | `#141416`（纯黑） | `#5423E7` / `#E62E4D` | 常规信息卡、代码路径卡、对比列 |
| **2. 电光超紫（Hyper Violet）** | `url(#violetBrutalGrad)` | `#FFFFFF`（纯白） | `#D8FF29`（酸性荧光黄绿） | 核心主张、封面主视觉、重点卡片 |
| **3. 酸性荧光绿（Kinetic Acid Lime）** | `url(#limeBrutalGrad)` | `#141416`（纯黑） | `#141416` 贴纸 + `#FFFFFF` 字 | 核心高亮、行动结论、警示或焦点模块 |
| **4. 波普珊瑚红（Bauhaus Coral）** | `url(#coralBrutalGrad)` | `#FFFFFF`（纯白） | `#FFD83D`（明黄）/ `#141416` | 拒绝项、异常报错、关键转折横幅 |
| **5. 赛博电光青（Cyber Cyan）** | `url(#cyanBrutalGrad)` | `#141416`（纯黑） | `#FFFFFF` 贴纸 + `#141416` 字 | 工具链、模型矩阵、并列分类 |
| **6. 终端炭黑（Terminal Carbon）** | `url(#carbonBrutalGrad)` | `#FFFFFF`（纯白） | `#D8FF29` / `#38E5FF` | 终端命令、目录总览、底层架构模块 |

> **铁律**：浅亮色底（纯白 `#FFFFFF`、酸性绿 `#D8FF29`、赛博青 `#38E5FF`、明黄 `#FFD83D`）上正文必须使用纯黑 `#141416`；深色或高饱和暖色底（电光紫、珊瑚红、终端炭黑）上正文必须使用纯白 `#FFFFFF`。

---

## 三、新粗野主义卡片构造（45° 硬阴影 + 窗口顶栏）

### 1. 标准波普卡片（45° 实体黑影 + 3px 黑框）
严禁使用 `<feDropShadow>` 模糊阴影！所有卡片立体感完全由右下方偏移 `dx="+7" dy="+7"` 的纯黑实体矩形（`#141416`）构成：

```xml
<g>
  <!-- 45° Diagonal Hard Shadow (+7px, +7px) -->
  <rect x="71" y="119" width="556" height="250" rx="16" fill="#141416" />
  <!-- Main Card Surface -->
  <rect x="64" y="112" width="556" height="250" rx="16" fill="#FFFFFF" stroke="#141416" stroke-width="3" />
</g>
```

### 2. OS 窗口顶栏卡片（Window Chrome Card）
在重点卡片顶部绘制 `36px` 高的窗口顶栏（带三枚几何圆点与粗黑横线），赋予极客 IDE / 数字工作台质感：

```xml
<g>
  <rect x="71" y="119" width="556" height="250" rx="16" fill="#141416" />
  <rect x="64" y="112" width="556" height="250" rx="16" fill="#FFFFFF" stroke="#141416" stroke-width="3" />
  <!-- Window Header Divider -->
  <line x1="64" y1="150" x2="620" y2="150" stroke="#141416" stroke-width="2.5" />
  <!-- 3 Geometric Window Dots -->
  <circle cx="90" cy="131" r="6" fill="#FF5470" stroke="#141416" stroke-width="2" />
  <circle cx="110" cy="131" r="6" fill="#FFD83D" stroke="#141416" stroke-width="2" />
  <circle cx="130" cy="131" r="6" fill="#D8FF29" stroke="#141416" stroke-width="2" />
</g>
```

### 3. 波普贴纸徽章（Brutalist Sticker Badge）
用于章节序号、核心图标或分类标签，带 `2.5px` 黑边与 `+3px, +3px` 硬阴影：

```xml
<g transform="translate(96, 172)">
  <rect x="3" y="3" width="54" height="54" rx="12" fill="#141416" />
  <rect x="0" y="0" width="54" height="54" rx="12" fill="url(#limeBrutalGrad)" stroke="#141416" stroke-width="2.5" />
</g>
```

---

## 四、字体与排版规范

1. **字体栈**：
   - 中文标题与正文：`-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif`
   - 英文 / 数字 / 序号：`'Arial Black', 'Helvetica Neue', 'SF Pro Display', sans-serif`
2. **字号与字重层级**：
   - **封面主标题**：`46px–54px`，`font-weight="900"`
   - **页面顶部大标题**：`32px–36px`，`font-weight="900"`，左侧配波普贴纸徽章（如带 `+4px` 硬阴影的荧光绿/珊瑚红方块）
   - **卡片主标题 / 核心结论**：`27px–34px`，`font-weight="900"`
   - **卡片正文**：`23px–26px`，`font-weight="800"`，行距 `38px–44px`
3. **装饰几何语汇**：
   - 使用纯粹的矢量波普图形（八角星芒、粗黑对角箭头 `↗`、等轴测方块、文件夹标签页、盾牌锁扣、显卡芯片阵列），不添加大纲以外的无关英文装饰词。
