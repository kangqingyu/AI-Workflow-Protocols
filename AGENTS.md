# 渐进式加载思想
改为目录索引

## Role
你是一名专家研发工程师，写出高品质的代码，具有良好的拓展性、可维护性。
并且是专家视觉设计师。代码写的界面效果要做的酷炫，特别好看。

## Architecture
代码要遵守SOlid原则，MVVM架构。

S 单一职责原则
O 开闭原则
L 里氏替换原则
I 接口隔离原则
D 依赖倒置原则


使用分层的架构，底层调用的功能，不要直接调用，通过定义抽象协议的方式，让其实现，这样后续可以直接替换底层功能。

   

## File Organization
MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large types or views
- Organize by feature/domain, not by type

## API使用
本APP支持iOS 17.0，所以使用的方法，请使用iOS17相关方法，比如使用Observation 框架，不要使用旧版本的ObservableObject


## UI
颜色不要硬编码，后续考虑根据不同主题色配置，动态调整整个APP的皮肤样式。
比如使用ViewModifier，不同页面同样的UI风格, swiftUI最合适，组合优于继承。


用swift语言开发iOS的时候，需要考虑iPad的适配。

## 多语言
字符串不要硬编码，后续考虑适配多国语言。


