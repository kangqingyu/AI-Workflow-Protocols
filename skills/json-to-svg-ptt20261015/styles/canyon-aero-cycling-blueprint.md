# 风格十三：Canyon × Rapha 破风车架几何工程蓝图 × 职业码表遥测风（Canyon Aero Frame Geometry Blueprint & Rapha Peloton Telemetry）

融合 Canyon / Specialized S-Works 车架几何工程规格书（CAD Frame Geometry & Wind-Tunnel Spec Sheet）、Garmin Edge / Wahoo 骑行码表遥测界面（Peloton Head-Unit Telemetry）与 Rapha / Bianchi 现代公路骑行文化美学。专为公路车选购、车架几何（Stack / Reach / STR）、Bike Fitting 人体工学度量、碳铝车架与套件对比、通勤路线与骑行装备主题打造。

---

## 1. 色彩与材质系统（Titanium Alloy & UD Carbon Palette）

| 角色 | 色值 | 视觉质感与用途 |
| :--- | :--- | :--- |
| **风洞钛银画布** | `#F3F5F8` → `#E8ECF2` → `#EFF2F7` | 冷调风洞实验室钛白/阳极氧化银灰渐变，搭配 `32×32` 毫米级 CAD 工程网格与十字准星，呈现精密机械质感 |
| **CNC 铝合金规格白卡** | `#FFFFFF`（描边 `#D9E0EC`，底部立体切角底座 `#C8D1E0`） | 阳极氧化铝切削白卡，承载车型参数、尺码几何、价格与优缺点对比 |
| **UD 碳纤破风主卡** | `#121620` → `#1C2333`（描边 `#2E3A52`） | 单向（UD）碳纤维暗黑斜纹质感卡，用于核心购车决策结论、关键骑行原则与重点警示 |
| **鲁贝竞速红（减震/制动/核心结论）** | `#E11D48`（浅底 `#FFF1F2`，描边 `#FECDD3`） | 致敬 Specialized Roubaix 与竞速涂装，用于核心结论、碟刹制动、预算锚点与关键警示 |
| **破风信号橙（通勤/路线/行动）** | `#EA580C`（浅底 `#FFF7ED`，描边 `#FED7AA`） | 致敬 Canyon / Wahoo 遥测高亮，用于 20km 通勤场景、车架几何改动、价格高亮与实操步骤 |
| **电变钴蓝（几何/Fitting/套件）** | `#1D4ED8`（浅底 `#EFF6FF`，描边 `#BFDBFE`） | 致敬 Shimano Ultegra / Di2 工业蓝，用于 Stack/Reach/STR 参数、Fitting 关节活动度与传动齿比 |
| **米兰松石青（舒适/绿道/养护）** | `#0D9488`（浅底 `#F0FDFA`，描边 `#99F6E4`） | 致敬 Bianchi Celeste 与城市绿道，用于耐力舒适性、平把视野、雨骑保养与羊毛/速干衣护理 |
| **正文主字色** | `#0F172A`（碳纤深黑）/ `#475569`（钛灰副文） | 高对比度工业规格书阅读体验；深色碳纤卡内使用 `#FFFFFF`、`#FDBA74`、`#5EEAD4` 与 `#93C5FD` |

---

## 2. 排版与单行主标题铁律（Typography & Head-Unit Bar）

1. **单行主标题铁律（严禁重复渲染 `part_title`）**：
   - 正文页顶部码表状态栏仅渲染 `pages[0].title` 作为唯一主标题（字号 `26px~30px`，字重 `800`）。
   - **严禁在主标题上方、下方或同卡片内再次渲染 `part_title` 小字**；目录页 `table_of_contents.title` 全页只渲染一次。
2. **骑行码表遥测顶栏（Cycling Head-Unit Telemetry Bar）**：
   - 顶栏左侧配置 CNC 金属立体徽章（如 `01`、`FIT`、`GEO`、`AL/CF`），顶栏右侧配置英文工程遥测胶囊（如 `COMMUTE // 20KM`、`BIKE FITTING // STR`、`ENDURANCE SPEC`）与等宽页码 `XX / 53`。
3. **字体栈**：
   - 中文标题与正文：`'PingFang SC', 'Hiragino Sans GB', 'SF Pro Display', sans-serif`
   - 车架尺码、价格、STR 几何比值与遥测铭牌：`'JetBrains Mono', 'SF Mono', monospace`

---

## 3. 标志性公路车视觉微组件（Signature Cycling Widgets）

- **700C 钻石车架 CAD 几何线框（700C Diamond Frame CAD Blueprint）**：精准勾勒头管、上管、立管、下沉式后上叉、前叉与前后轮组同心圆，辅以 `STACK` / `REACH` 工程虚线标尺。
- **车型报价与传动规格铭牌（Spec & MSRP Pill）**：将笔记中的价格（如 `2398 元`、`¥8,580`）、速别（`2×10`、`Sora 9 速`）与胎宽（`700×32C`）封装为工业铭牌样式，清晰易读。
- **碳纤斜纹光影肌理（UD Carbon Weave Pattern）**：深色卡片叠加低透明度 45° 碳布斜纹，赋予页面真实的碳纤维公路车工业质感。
