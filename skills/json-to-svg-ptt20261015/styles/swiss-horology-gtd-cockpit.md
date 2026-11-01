# 风格十：瑞士精密制表 × OmniFocus/Things 3 现代效能工作台风（Swiss Horology & Zen Productivity Cockpit）

## 1. 风格定位与美学灵感

- **核心气质**：心如止水（Mind Like Water）、瑞士精密计时（Swiss Chronograph Precision）、Apple Design Award 级效能工作台（Things 3 & OmniFocus 4 Cockpit）、大脑内存减负（Brain RAM Offloading）。
- **设计灵感**：
  - **Things 3 (Cultured Code) & OmniFocus 4 (The Omni Group)**：荣获 Apple 设计大奖的现代 macOS/iOS 效能界面美学——纯净通透的钛银冰白工作台、圆润精致的交互式任务复选框（Checkbox Ring）、多维场景胶囊标签（Context Tag Pills）与“延迟到（Defer）”时间轴。
  - **瑞士精密计时码表（IWC / Braun Horology Chronograph）**：60 分钟精密刻度表盘外圈、`25min + 5min` 番茄钟双色计时扇区、游标卡尺级微米刻度线，赋予“时间管理”看得见的机械秩序感。
  - **GTD「心如止水（Mind Like Water）」与契可尼效应内存条**：用静谧扩散的止水同心波纹与“大脑后台进程 RAM 释放指示器”，将抽象的认知心理学与时间流水线转化为直观的视觉语言。
- **适用场景**：GTD 时间管理系统、个人效能与精力管理、工作流自动化、项目管理、专注力与番茄工作法、数字工具方法论。

---

## 2. 色彩系统（钛银止水白 × 瑞士计时蓝 × 效能紫晶 × 番茄活力橙 × 禅意翡翠绿）

| 角色 | 颜色名称 | Hex / 渐变建议 | 用途说明 |
|---|---|---|---|
| **画布主背景** | 钛银冰川白 → 止水冷雾白 | `#F5F8FC` → `#ECF2F9` → `#F3F6FB` | 1280×720 画布基底，营造清爽、零压力的现代效能桌面 |
| **深色中枢卡底** | 深海计时表盘黑蓝 | `#0F172A` → `#1E293B` | 封面主视觉、核心流水线横幅、重点总结暗色中枢卡片 |
| **普通卡片基底** | 纯净工作台白 | `#FFFFFF`（92%–98% 不透明度） | Bento 任务卡片主体，配 `#DCE5F0` 精细描边与柔和悬浮阴影 |
| **次级卡片基底** | 冰川浅灰蓝 | `#F8FAFC` / `#F1F5F9` | 子任务分组框、场景过滤槽、对比说明区底色 |
| **主标题/正文墨色** | 钛黑深邃墨色 | `#0F172A` | H1、H2、卡片主标题、核心结论文字 |
| **常规正文色** | 石板灰蓝正文色 | `#334155` | 正文列表、任务细项说明（高对比度、长时阅读不疲劳） |
| **次要元数据色** | 计时冷灰 | `#64748B` | 页码刻度、表盘刻度数字、辅助标签说明 |
| **主强调色 A（GTD 秩序/捕捉）** | 瑞士计时蓝（Inbox Blue） | `#1D63DC`（浅底色 `#EBF2FE`） | GTD 主流程、Step 1 捕捉、系统架构、主标题色标 |
| **主强调色 B（组织/筛选/延迟）** | OmniFocus 效能紫晶 | `#6D4AFF`（浅底色 `#F1EEFF`） | Step 2 处理与组织、8 大清单分类、“延迟到（Defer）”功能 |
| **主强调色 C（番茄钟/瓶颈/警示）** | 番茄计时橙（Chrono Orange） | `#EA580C`（浅底色 `#FFF1E8`） | 番茄工作法 25+5、契可尼后台占用警示、第一象限紧急任务 |
| **主强调色 D（心如止水/回顾/完成）** | 禅意翡翠绿（Mindful Teal） | `#0D9488`（浅底色 `#E6F7F5`） | Step 3 回顾、Step 4 执行完成态、心如止水状态、习惯养成 |

---

## 3. 排版与字体规范

- **现代几何无衬线标题体（Precision Sans-Serif）**：
  - `font-family: 'PingFang SC', 'SF Pro Display', 'Hiragino Sans GB', 'Microsoft YaHei', system-ui, sans-serif`
  - 用于：封面大标题、每页单行主标题、Bento 卡片标题（H2/H3），呈现干净利落的现代软件质感。
- **高可读正文体（Clean UI Body）**：
  - `font-family: 'PingFang SC', 'SF Pro Text', 'Hiragino Sans GB', system-ui, sans-serif`
  - 用于：任务清单项、层级列表、方法论拆解。
- **精密计时等宽体（Chronograph Monospace）**：
  - `font-family: 'JetBrains Mono', 'SF Mono', 'Menlo', monospace`
  - 用于：页码（`01 / 31`）、番茄钟倒计时（`25:00` / `05:00`）、步骤编号（`STEP 01`–`STEP 04`）、2 分钟原则（`< 120s`）。
- **字号层级约束**：
  - 页面单行主标题：`28px–32px`（字重 `800`）
  - 卡片标题（H2）：`19px–22px`（字重 `700`）
  - 卡片子标题（H3）：`16px–18px`（字重 `700`）
  - 卡片正文列表：`15px–17px`（字重 `500`，行距 `26px–30px`）

---

## 4. 标志性视觉组件（Signature Components）

### 4.1 效能工作台任务卡片（Productivity Cockpit Bento Card）
- 每张 Bento 卡片顶部或左侧配有 `6px–8px` 宽的**状态色标条（Status Accent Bar）**，右上角可点缀枚小巧的**场景/状态胶囊（Context Tag Pill）**或精密计时图标。
- 列表要点前采用 **Things 3 / OmniFocus 风格圆角复选框（Checkbox Ring）** 或带编号的胶囊徽章，替代呆板的普通圆点。

### 4.2 瑞士计时码表与番茄钟刻度环（Swiss Chronograph & Pomodoro Bezel）
- 在画布背景右上角及时间/节奏相关页面，绘制精细的**同心计时表盘刻度圈（60 格微米刻度 + `25min / 5min` 扇区弧线）**，呼应“创造更多时间”与番茄工作法。

### 4.3 「心如止水」同心波纹与大脑 RAM 内存释放条（Mind Like Water & RAM Meter）
- 用极淡的静水同心波纹体现 GTD 清空大脑后的平静状态；在讲解“契可尼效应”或“任务过多纠结”时，可搭配直观的后台内存释放/负载仪表条装饰。

### 4.4 单行主标题顶栏（Single-Line Chronograph Header）
- 正文页左上角**只渲染单行页面主标题（`pages[0].title`）**，左侧搭配瑞士计时蓝/紫晶/翡翠绿竖向胶囊色标；**严禁在主标题上方再输出一行 `part_title` 小字**（彻底杜绝“第一行小字、第二行大字”的重复标题）。目录页同理，`目录` 全页只出现一次。

---

## 5. 页面布局与核心红线

1. **画布尺寸固定**：`viewBox="0 0 1280 720" width="1280" height="720"`。
2. **文字完整性**：严格保留 JSON 大纲中的全部正文文字与层级结构，不遗漏任何要点，也不凭空添加大纲外的解释文字。
3. **Bento 网格间距**：卡片间距不少于 `20px`，四周安全边距不少于 `48px`（推荐左右边距 `56px`）。
4. **真实图片内嵌**：遇到 `图片（使用附件中图片：xxx）` 或 `asset_refs` 时，将其转化为带**macOS 原生窗口/视网膜画框**的真实 Base64 Data URI `<image>`，不把图片提示语当作正文输出。
