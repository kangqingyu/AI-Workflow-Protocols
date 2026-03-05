---
name: fix-compile-error
description: 开发完成编译检测，查看报错问题并修复。0212
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash(xcodebuild *, git *, tree, find, grep, rg, sed, nl, basename)
---

# fix-compile-error

# 编译检测目标
 
step1 具体项目名字，项目路径，请根据如下文件查看：
/Users/kqy/Documents/kqyCode/Workspace/.claude/skills/repo-dir-list/SKILL.md

step2 确定项目名称之后，先用 `xcodeproj` 快速定位 Swift 语法问题，再用 `xcworkspace` 做最终验收（尤其是 CocoaPods 工程）。


# 编译检测推荐命令（先快后准）
先定义变量（根据 step1 查到的具体项目填写）：
```bash
APP_ROOT="/path/to/your/app"
PROJECT_NAME="YourProject"
SCHEME_NAME="YourScheme"
SIM_DEST_QUICK="generic/platform=iOS Simulator"
SIM_DEST_FINAL="platform=iOS Simulator,name=iPhone 16"
BUILD_LOG="/tmp/${PROJECT_NAME}_build.log"
```

### A. 快速抓 Swift 编译错误（适合先定位语法）
```bash
cd "$APP_ROOT" && \
xcodebuild -project "${PROJECT_NAME}.xcodeproj" \
  -scheme "$SCHEME_NAME" \
  -configuration Debug \
  -destination "$SIM_DEST_QUICK" \
  build > "$BUILD_LOG" 2>&1 || true; \
rg -n "error:|warning:" "$BUILD_LOG" | sed -n '1,220p'
```

### B. 最终验收（Pods 链接与真实工程）
```bash
xcodebuild -workspace "${APP_ROOT}/${PROJECT_NAME}.xcworkspace" \
  -scheme "$SCHEME_NAME" \
  -destination "$SIM_DEST_FINAL" \
  build 2>&1 | tail -140
```

### C. 查看具体报错上下文
如果知道具体报错文件路径，可直接查看报错行上下文
```bash
nl -ba <relative-or-absolute-file-path>.swift | sed -n '190,210p'
```

## 标准执行顺序
1. 跑 A 命令，快速收敛 Swift 语法错误。
2. 修复代码后重复 A，直到无 Swift `error:`。
3. 跑 B 命令，确认 Pods 链接与 workspace 构建通过。
4. 如果 B 失败但 A 通过，优先判断为环境或 Pods/链接问题，而非业务 Swift 语法问题。


# CoreSimulator 异常的原因与处理
常见原因：
- CoreSimulator 后台服务异常（`simdiskimaged` 崩溃/无响应）
- 沙箱或目录权限限制，导致临时文件/缓存目录不可写
- Xcode 运行态缓存或模拟器运行时索引异常

处理建议：
1. 先用 `xcodeproj + generic simulator` 获取可修复的 Swift 报错。
2. 代码修复后，切回 `xcworkspace` 做最终 build。
3. 若仍报 CoreSimulator 异常，优先排查本机环境（服务状态、权限、缓存目录可写性）。




# 关于“在 Skills 中设置权限避免询问”
关键结论：
- `SKILL.md` 的 `allowed-tools` 只能限制“可用工具范围”，不能直接绕过沙箱升级确认。
- 真正免重复询问依赖运行时的 `Approved command prefixes`。

正确做法：
1. 第一次执行关键命令时，用 `sandbox_permissions=require_escalated` 请求授权。
2. 同时提交稳定 `prefix_rule`（命令前缀）。
3. 用户确认后，该前缀会进入 `Approved command prefixes`，后续同前缀自动执行。

推荐前缀（按项目替换）：
- `xcodebuild -project <PROJECT_NAME>.xcodeproj -scheme <SCHEME_NAME>`
- `xcodebuild -workspace <APP_ROOT>/<PROJECT_NAME>.xcworkspace -scheme <SCHEME_NAME>`



# 常见问题总结
2. 运行环境问题（非业务代码）
- 现象：`CoreSimulatorService connection became invalid`、`simdiskimaged crashed or is not responding`、`unable to make temporary file`。
- 这类问题会让 `xcodebuild` 误报为 workspace/project 解析失败，或无法稳定进入编译阶段。

3. CocoaPods 链接差异
- `xcodeproj + generic simulator` 可快速暴露 Swift 语法问题。
- 但最终链接（`UMCommon`/`UMDevice` 等 Pods Framework）必须以 `xcworkspace` 为准。
