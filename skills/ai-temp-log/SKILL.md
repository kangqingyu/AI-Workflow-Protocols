---
name: ai-temp-log
description: 处理 iOS/Swift 开发中所有的临时调试、日志打印需求。当被要求“打印日志”、“调试这段逻辑”或需要输出变量状态时，必须触发此技能，强制使用 AITempLog 命名空间，严格禁止使用原生 print() 或 os.Logger。
---

# AI Temp Log Standard (临时调试日志规范)

## 🎯 Core Directive (核心纪律)
在当前工程中，**绝对禁止**在业务代码中使用原生的 `print()`、`NSLog()` 或 `os.Logger` 来输出任何临时性质的调试信息。
所有的临时调试日志，必须统一路由至全局命名空间 `AITempLog`，并以当前正在开发的**需求/特征 (Feature)** 为维度进行严格的物理隔离。

## 🛠️ Execution Steps (执行步骤)

### 1. Identify Feature (识别当前上下文)
明确当前正在开发的具体业务需求或功能模块。例如：如果是文学作品人物关系图谱的渲染模块，则 feature 为 `characterGraph`。


### 2. Check Namespace (检查/定义命名空间)
如果在项目中找不到 `AITempLog.swift` 文件，或者该文件中没有当前开发需求的专属方法，请在 `AITempLog` 枚举中自动补充定义。
**定义规范：**
- 必须为 `static func`。
- 方法名必须清晰对应当前开发需求（使用小驼峰命名）。
- 内部实现必须被 `#if DEBUG` 包裹，确保线上安全。
- 打印格式需包含高亮 Emoji 和需求前缀标签。

```swift
// AITempLog.swift (全局调试中心参考实现)
enum AITempLog {
    // 当前开发需求示例
    static func characterGraph(_ msg: Any, file: String = #file, line: Int = #line) {
        #if DEBUG
        print("🤖 [AI-CharacterGraph] [\(URL(fileURLWithPath: file).lastPathComponent):\(line)] -> \(msg)")
        #endif
    }
}