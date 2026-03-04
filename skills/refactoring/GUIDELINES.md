# 代码规范

## 整体原则

(IMPORTANT!)
**谨记遵循如下软件设计的最佳实践**

- 编程追求清晰理念，更少的代码代表着更大的信息密度，但是一定不要牺牲可读性，因为代码最重要的还是可读性
- 先简单算法和基础数据结构，测过瓶颈再优化，数据结构比算法更关键
- **多用数据驱动理念**，把复杂逻辑写成表而非一堆判断
- 代码中的数据也应该集中，便于理解和修改
- 变量名追求清晰而非越长越好，全局名详细、局部名精简，命名统一
- 函数名要体现行为或返回值，让调用处语义清晰
- 少写注释，代码自解释；只在关键处加简介，避免冗余注释
- 故障导向安全：例如校验失败应该阻止而非放行
- DRY：Don’t Repeat Yourself
- KISS：Keep It Simple, Stupid
- YAGNI：You Ain’t Gonna Need It
- SOLID：单一职责、开闭原则、里氏替换、接口隔离、依赖倒置
- LoD：迪米特法则（最少知道）
- Fail Fast：快速失败，早报错
- High Cohesion, Low Coupling：高内聚、低耦合
- Single Source of Truth：单一数据源

## 关于重构

- 每次开发后思考要不要小范围重构是个好习惯
- 重构的基础是良好的自动化测试，所以测试很重要

## 其他参考

### Zen of Python

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one-- and preferably only one --obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than *right* now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea -- let's do more of those!
