# 风格十二：医学 3.0 生命体征仪表盘 × 北欧自然疗愈风（Medicine 3.0 Longevity Biometrics & Mindful Sanctuary）

融合 Peter Attia《Outlive（超越百岁）》医学 3.0 健康寿命（Healthspan）图表美学、Oura Ring / Apple Health / Whoop 现代生物体征监测仪表盘（Biometric Telemetry）与北欧自然疗愈呼吸感（Nordic Mindful Sanctuary）。专为长寿医学、运动生理（VO₂ max / Zone 2 / 稳定性 / 力量训练）、精准营养与血糖监测（CGM）、睡眠神经修复与正念冥想觉察主题打造。

---

## 1. 色彩与材质系统（Biometric & Botanical Palette）

| 角色 | 色值 | 视觉质感与用途 |
| :--- | :--- | :--- |
| **画布底色** | `#F6F5F0` → `#ECEAE2` → `#F3F1EA` | 温润生机亚麻米白渐变，搭配 `36×36` 生理坐标微网格与十字准星，兼顾实验室精度与自然疗愈感 |
| **主白卡片** | `#FFFFFF`（描边 `#DEDAD0`，底部立体底座 `#D6D2C6`） | 纯净医疗级磨砂白卡片，承载核心正文、步骤清单与白底医学图谱 |
| **深林生命中枢卡** | `#13221E` → `#1B2E28`（描边 `#2C473E`） | 森林深绿/午夜生物黑渐变，用于核心洞见、神经网络（DMN/CEN）、睡眠修复与重点警示卡 |
| **生机翠绿（有氧/健康寿命）** | `#0F8A65`（浅底 `#ECFDF5`，描边 `#A7F3D0`） | 代表医学 3.0 健康寿命跃升、VO₂ max、Zone 2 二区有氧、蔬菜与呼吸 |
| **心血管珊瑚红（风险/骨骼警示）** | `#E04F3E`（浅底 `#FEF2F2`，描边 `#FECACA`） | 代表慢性病“四骑士”、L4–L5/L5–S1 腰椎压力、不良姿势与愤怒触发点 |
| **昼夜节律靛蓝（睡眠/脑科学）** | `#3B4CCA`（浅底 `#EEF2FF`，描边 `#C7D2FE`） | 代表深度睡眠、Aβ/Tau 蛋白清理、DMN/CEN 脑网络、觉察与元认知 |
| **代谢暖阳琥珀（力量/营养/习惯）** | `#D97706`（浅底 `#FFFBEB`，描边 `#FDE68A`） | 代表力量训练、底盘稳定性、蛋白质/碳水配比与日常微习惯 |
| **正文主字色** | `#141E1B`（深林炭黑）/ `#4A5A54`（次级灰绿） | 高对比度阅读体验，深色卡内正文使用 `#FFFFFF` 与 `#A7F3D0` / `#FDBA74` |

---

## 2. 排版与单行主标题铁律（Typography & Single-Line Title Rule）

1. **单行主标题铁律（严禁重复渲染 `part_title`）**：
   - 内容页顶部状态栏仅渲染 `pages[0].title` 作为唯一主标题（字号 `25px~30px`，字重 `800`）。
   - **严禁在主标题上方、下方或同卡片内再次输出 `part_title` 小字**，杜绝“第一行小字、第二行大字”的重复现象。
2. **生物体征胶囊标签（Biometric Telemetry Badge）**：
   - 顶栏左侧配置立体圆角章节徽章（如 `8.1`、`8.2`、`MED`），顶栏右侧配置英文生理监测遥测胶囊（如 `HEALTHSPAN // MED 3.0`、`VO2 MAX & ZONE 2`、`SPINE BIOMECHANICS`）及等宽页码 `XX / 37`。
3. **字体栈**：
   - 中文标题与正文：`'PingFang SC', 'Hiragino Sans GB', 'SF Pro Display', sans-serif`
   - 生理指标、章节编号与遥测标签：`'JetBrains Mono', 'SF Mono', monospace`

---

## 3. 标志性微组件（Signature Biometric Widgets）

- **健康寿命双轨曲线微图（Healthspan Curve Widget）**：展示传统衰退曲线与医学 3.0 平台期跃升曲线的对比。
- **生理环与心率区间条（Zone 2 & VO₂ Max Bar）**：采用分段式生机翠绿/琥珀色能量条与脉冲波形修饰卡片。
- **医学图谱与实拍画框（Medical Atlas Frame）**：针对原文内嵌图片（如健康寿命曲线、脊椎分段、腰椎间盘突出、横膈膜呼吸等），使用纯净白底内衬框 + 圆角 `clipPath` + `preserveAspectRatio="xMidYMid meet"` 完整展示原图细节，绝不裁切坐标轴或图注。
