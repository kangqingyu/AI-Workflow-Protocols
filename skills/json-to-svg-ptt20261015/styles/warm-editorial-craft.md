# 智性暖纸书卷风（Warm Editorial Craft & Botanical Ink）

仅在选中本风格时读取。画布、内容忠实度和图片处理要求遵循 `SKILL.md` 的核心约束。

## 布局与装帧网格架构

- 将画布视为一页典藏级人文杂志或美术馆展览图录（Archival Editorial Spread），推荐卡片间距 `24–28px`，卡片圆角 `rx="16–20"`。
- **四态典藏纸墨卡片交替排布**：组合使用 **亚麻棉白书页卡（Archival Linen）× 典藏深林墨绿卡（Botanical Forest）× 朱砂赤陶主卡（Terracotta Cinnabar）× 胡桃炭墨卡（Walnut Espresso）**，营造兼具人文厚度、智性思辨感与呼吸留白的书卷气质。
- **双线装帧内框（Double-Rule Bookplate Frame）**：重点模块或大号卡片内部可内缩 `10px` 叠加一层 `0.8px` 半透明细线内框（`rx="10–12"`），呼应古典书籍装帧与展览铭牌细节。

## 亚麻画布与纸墨卡片参数

| 元素 / SVG 标识 | 参数规范 |
|---|---|
| 典藏亚麻棉纸画布 `paperCanvasGrad` | 线性渐变：`#F6F2EA`（0%）→ `#EFE9DC`（55%）→ `#E6DEC8`（100%） |
| 建筑装帧细线网格 `editorialGrid` | `40 × 40` `<pattern>`：`0.5px` 暖灰细线 `#D8CFC0`（`opacity="0.45"`）+ 交叉点微菱形或圆点 `#BFB4A3` |
| 画布外框与书页裁切线 | 外周 `x="22" y="22" width="1236" height="676" rx="12"` 双层装帧细线（外线 `#C8BDAE` `1.2px`，内缩 `4px` 细线 `#DCD4C6` `0.75px`），四角配古典十字星芒裁切标 |
| 典藏深林墨绿卡 `forestCardGrad` | 线性渐变：`#214637` → `#163328` → `#0F241C`；底部配向下偏移 `6px` 的 `#091711` 书脊厚底，外框 `#2E5C49` |
| 朱砂赤陶主卡 `terracottaCardGrad` | 线性渐变：`#CC563B` → `#B54027` → `#99311B`；底部配向下偏移 `6px` 的 `#6E2010` 厚底，外框 `#E07158` |
| 胡桃炭墨卡 `espressoCardGrad` | 线性渐变：`#2A2420` → `#1E1A17` → `#151210`；底部配向下偏移 `6px` 的 `#0B0908` 厚底，外框 `#3E3630` |
| 亚麻棉白书页卡 `linenCardGrad` | 线性渐变：`#FFFDF9` → `#F7F2E8`；底部配向下偏移 `6px` 的 `#CFC5B4` 叠纸底座，外框 `#FFFFFF` |
| 温润纸张投影 `editorialShadow` | `<feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#2A2118" flood-opacity="0.16" />` |

## 智性书卷色板与古典几何微件

| 色名 | 色值 | 适用角色 |
|---|---|---|
| 朱砂赤陶（Terracotta Cinnabar） | `#C84B31` / `#B54027` | 核心命题强调、火漆印章底座、棉白卡片重点高亮字 |
| 典藏深林绿（Botanical Forest） | `#1B4332` / `#2D6A4F` | 深度逻辑卡片、植物理性徽章、棉白卡次级重点字 |
| 香槟暖金（Champagne Gold） | `#E6C365` / `#C59B27` | 深林绿/炭墨卡片上的标题高亮、星芒罗盘、双线内框 |
| 鼠尾草青（Sage Celadon） | `#74C69D` / `#52B788` | 深色卡片上的演进链路、正向反馈节点与平衡几何 |
| 胡桃浓墨（Walnut Ink） | `#1C1815` / `#5C5349` | 亚麻棉白卡片上的主标题、正文与次级注释 |

### 标志性书卷几何微件（纯矢量，不添加大纲外文字）

- **四角星芒与古典星盘（Editorial Starburst & Astrolabe）**：使用二次贝塞尔曲线 `M 0,-20 Q 0,0 20,0 Q 0,0 0,20 Q 0,0 -20,0 Q 0,0 0,-20 Z` 绘制四角星芒，外围环绕 `stroke-dasharray="3 4"` 的精密星轨虚线环。
- **拱门书签章与火漆印章底座（Arched Bookplate & Wax Seal）**：图标容器采用顶部半圆拱门形（Arch）或带内缩金线的方形藏书票底座，赋予极强的文化出版物辨识度。
- **古典天平、月相与植物几何（Classical Balance, Moon Phases & Botanical Geometry）**：用对称圆弧、交叠透镜（Vesica Piscis）与黄金分割线表达思辨、边界与系统平衡。
- **人文排版张力**：主标题与金句可结合高字重衬线/宋体与现代无衬线字体栈（`'Songti SC', 'STSong', 'Noto Serif SC', 'PingFang SC', serif`），拉大行高与字距，营造纸质出版物的阅读呼吸感。
