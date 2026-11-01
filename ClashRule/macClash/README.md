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
