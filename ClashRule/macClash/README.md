# FlClash 自定义规则集（GitHub 唯一数据源 + 本地 0 秒同步）

本目录维护 FlClash（Mihomo 内核）远程 `rule-providers` 数据源、扩展覆写脚本与本机零延迟同步脚本。

## 文件职责

| 文件 | 用途 | GitHub Raw URL |
| :--- | :--- | :--- |
| `Direct.yaml` | `DIRECT` 直连规则数据源 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/Direct.yaml` |
| `Reject.yaml` | `广告站点`（可切 `REJECT` / `DIRECT`）数据源 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/Reject.yaml` |
| `FlClashOverride.js` | FlClash 脚本覆写配置 | `https://raw.githubusercontent.com/kangqingyu/AI-Workflow-Protocols/main/ClashRule/macClash/FlClashOverride.js` |
| `sync_local_flclash.sh` | 本机保存 YAML 后 0 秒同步至 FlClash 缓存 | — |

## 两大核心特性

1. **在 FlClash 面板随时切换 `REJECT` / `DIRECT`**
   - `KqyReject` 已绑定至订阅自带的 **「广告站点」** 策略组。
   - 在 FlClash 左侧 **代理 ➔ 广告站点** 中，可随时点选切换 **`REJECT`**（屏蔽）或 **`DIRECT`**（直连放行），0 秒立即生效。
2. **本地修改 YAML 0 秒同步（无需干等 GitHub 3~5 分钟）**
   - 本机已配置 macOS `LaunchAgent` (`~/Library/LaunchAgents/com.kqy.flclash.rulesync.plist`) 自动监听 `Direct.yaml` 与 `Reject.yaml`。
   - 编辑器按下 `Cmd + S` 保存文件后，0.1 秒内自动同步写入 FlClash 本地缓存。
   - 需要跨设备同步或备份时，再执行 `git commit && git push` 即可。
