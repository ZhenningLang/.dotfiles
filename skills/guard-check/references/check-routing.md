# Check routing

## 路由原则

1. 先看当前 diff 的范围和风险
2. 默认调用 `guard-review`
3. 满足以下任一条件时追加 `guard-secure`
   - 身份认证
   - 权限控制
   - 外部输入
   - secrets / tokens / headers / cookies
4. 用户要求“验证通过 / 可以交付 / 可以合并”时追加 `guard-verify`
5. 需要 PR、发布、交付动作时切到 `guard-ship`

## 输出要求

- 明确本次走了哪些链路
- 给出最终裁决：`Ready` / `With fixes` / `Blocked`
- 如果没走某条链路，要写原因
