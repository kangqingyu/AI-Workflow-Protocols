# FlClash 自定义规则集（GitHub 唯一数据源）

本目录维护 FlClash（Mihomo 内核）远程 `rule-providers` 数据源与扩展覆写脚本。

## 文件职责

| 文件 | 用途 | GitHub Raw URL |
| :--- | :--- | :--- |
| `Direct.yaml` | `DIRECT` 直连规则数据源 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/Direct.yaml` |
| `Reject.yaml` | `REJECT` 拦截规则数据源 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/Reject.yaml` |
| `FlClashOverride.js` | FlClash 脚本覆写配置 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/FlClashOverride.js` |

## 首次在 FlClash 中挂载步骤

1. 打开 **FlClash** ➔ **工具（Tools）** ➔ **脚本（Script）**（或覆写设置）。
2. 新建脚本（如命名为 `GitHubCustomRules`），将 `FlClashOverride.js` 的内容粘贴进去并保存（也可通过脚本 Raw URL 导入）。
3. 进入 **配置（Profiles）** ➔ 点击当前机场订阅卡片右上角菜单 ➔ 选择覆写方式为 **脚本** 并勾选 `GitHubCustomRules`。
4. 点击更新一次订阅即可生效。

## 日常更新规则流程

1. 编辑 `Direct.yaml` 或 `Reject.yaml`（注意：**每行只写匹配类型与域名/IP，不要在行尾加 `,DIRECT` 或 `,REJECT`**）。
2. 提交并推送至 GitHub `main` 分支。
3. 自动同步：FlClash 每小时自动拉取更新；
   手动立即同步：推送约 3~5 分钟后，在 FlClash **外部资源（Providers）** 页面点击 `KqyDirect` / `KqyReject` 右侧的刷新按钮即可。









已在 **FlClash** 客户端中完成全部配置并实时生效：

### 1. 已完成的客户端操作
- **创建覆写脚本**：已在 FlClash「覆写 ➔ 脚本」中新建并保存 **`GitHubCustomRules`**（内容与 [FlClashOverride.js](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/FlClashOverride.js) 完全一致）。
- **双订阅全绑定**：已将你当前使用的 **`jogging.yaml`** 以及备用的 **`dounai.yaml`** 两个订阅均切换为「🚀 脚本」覆写模式，并勾选绑定 `GitHubCustomRules`（后续切换机场订阅也无需重复配置）。

### 2. 内核生效验证结果
已核验本机运行中的 [config.yaml](file:///Users/kqy/Library/Application%20Support/com.follow.clash/config.yaml) 与内核规则集缓存目录：
- **远程规则集拉取成功**：`KqyDirect`（723B）与 `KqyReject`（550B）均已由内核通过 `默认节点` 从 GitHub Raw 成功下载并加载。
- **置顶优先级生效**：`RULE-SET,KqyReject,REJECT` 与 `RULE-SET,KqyDirect,DIRECT` 已注入 `rules` 列表最顶部（例如此前在连接记录中误走代理兜底的 `tracker.m-team.cc` 现已命中 `KqyDirect` 直连）。

### 3. 日常维护提示
后续新增直连或屏蔽域名时，只需编辑 [Direct.yaml](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/Direct.yaml) 或 [Reject.yaml](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/Reject.yaml) 并 `git push`：
- **自动同步**：每小时自动更新；
- **手动立即更新**：推送约 3~5 分钟后，在 FlClash 左侧 **工具 ➔ 资源** 中点击 `KqyDirect` / `KqyReject` 的刷新按钮即可。







换新电脑（无论是另一台 Mac，还是 Windows / Linux / Android 端的 FlClash）有两种非常省事的方式：
### 方式一：一键整体迁移（最推荐，连机场订阅都不用重配）
FlClash 自带完整的备份同步机制：
1. 在当前电脑打开 FlClash ➔ **工具 ➔ 备份与恢复**，导出备份文件（或配置 WebDAV 云同步）。
2. 在新电脑安装 FlClash 后导入恢复，你的**机场订阅 + `GitHubCustomRules` 脚本 + 订阅绑定关系**会一次性全部还原，开箱即用。

---

### 方式二：全新手动挂载（只需 30 秒，甚至无需在新电脑 clone 仓库）
如果新电脑只是“使用规则”而不改代码，连 Git 仓库都不用拉取：
1. 在新电脑导入机场订阅并开启代理连接。
2. 进入 **配置 ➔ 订阅右上角 `⋮` ➔ 更多 ➔ 覆写 ➔ 🚀 脚本 ➔ 前往配置脚本 ➔ 添加**。
3. 粘贴 [FlClashOverride.js](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/FlClashOverride.js) 的内容（或点击右上角 `⋮ ➔ 外部获取 ➔ 通过URL导入`，填入 [README.md](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/README.md) 里记录的脚本 Raw 链接），保存后返回勾选该脚本即可。

之后无论你在哪台电脑上修改 [Direct.yaml](file:///Users/kqy/Documents/kqyCode/Workspace/AICodingProtocol/AI-Workflow-Protocols/ClashRule/macClash/Direct.yaml) 并 `git push`，所有绑定了该脚本的设备都会自动同步最新规则。