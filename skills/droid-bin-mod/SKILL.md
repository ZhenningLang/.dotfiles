---
name: droid-bin-mod
description: 修改 droid 二进制以禁用截断和解锁功能。当用户提到：修改/恢复/测试 droid、press Ctrl+O、output truncated、显示完整命令或输出时触发。
---

# Droid Binary Modifier

修改 Factory Droid CLI 二进制文件，禁用命令/输出截断，实现默认展开显示。

## 使用流程

### 如果用户说"测试"或"测试droid修改"

**直接执行以下命令验证修改效果，不要询问：**

```bash
# 测试 mod1 (命令截断) - 100字符命令应完整显示，无 "press Ctrl+O" 提示
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" && echo done

# 测试 mod4 (diff行数) - 需要编辑文件看diff
seq 1 100 > /tmp/test100.txt
```

然后执行：把 `/tmp/test100.txt` 的第1-100行全部替换成 `A1` 到 `A100`，diff 应显示超过20行（原来限制20行）。

### 如果用户说"修改"或"恢复"

**询问用户需要哪些修改：**

```bash
┌────────────────────────────────────────────────────────────────────┐
│ EXECUTE  (echo "aaa..." command truncated. press Ctrl+O)  ← mod1   │
│ line 1                                                             │
│ ...                                                                │
├────────────────────────────────────────────────────────────────────┤
│ EDIT  (README.md) +10 -5                                           │
│ ... (truncated after 20 lines)                            ← mod4   │
│ ... output truncated. press Ctrl+O for detailed view               │
└────────────────────────────────────────────────────────────────────┘

mod1: 命令框 "command truncated. press Ctrl+O" 提示 → 隐藏
mod4: Edit diff/输出截断行数 20 行 → 99 行
mod6: Ctrl+N 只在非 Copilot custom model 间切换 (跳过 ID 含 [ 的模型, /model 菜单不受影响)
mod7: 多行历史记录按↓无法返回空输入框 → 修复
mod8: Welcome 页面全部文字橙色 + 版本号后加 "Modified" 标记
mod9: Custom model 支持完整 effort 级别 (追加 "max", wUT() 自动映射 openai "xhigh")
mod10: Kitty keyboard 检测超时 200→999ms (缓解 iTerm2 竞态条件)

注：mod9 追加 "max" 到 effort 数组，wUT() 内置 "max"→"xhigh" 映射自动处理 openai
注：mod10 增大 kitty 协议检测窗口，降低终端响应泄漏概率

select: 1,4,6,7,8,9,10 / all / restore
```

用户选择后，执行对应修改。

## 版本适配说明

**混淆 JS 的应对策略**：变量名/函数名会变，但**字符串常量和代码结构不变**。

### 第一步：用不变的字符串定位

```bash
# 修改1: 用 isTruncated 定位截断函数
strings ~/.local/bin/droid | grep "isTruncated"

# 修改4: 用 [truncated] 和 VAR=2000 定位 diff 行数
strings ~/.local/bin/droid | grep -E "var [A-Za-z_$]+=20,[A-Za-z_$]+=2000"
```

### 第二步：用模式匹配确认

定义 JS 变量名模式: `V = [A-Za-z_$][A-Za-z0-9_$]*` (适应任意混淆结果)

| 修改项      | 不变的定位字符串 | 匹配模式（正则）                        | v0.89.0 实例              |
| ----------- | ---------------- | --------------------------------------- | ------------------------- |
| 1 截断条件  | `isTruncated`    | `if\(!V&&!V\)return\{text:V,isTruncated:!1\}` | `if(!L&&!D)return{text:H,isTruncated:!1}` |
| 4 diff 行数 | `=2000` (伴生变量) | `var V=20,V=2000`                      | `var iIq=20,dIq=2000`     |

## 修改原理

### 修改 1: 截断函数条件 (核心)

**原始代码**:

```javascript
function JZ9(A, R=80, T=3) {       // R=宽度限制80字符, T=行数限制3行
  if (!A) return {text: A||"", isTruncated: !1};
  let B = A.split("\n"),
      H = B.length > T,            // H: 是否超过行数限制
      Q = A.length > R;            // Q: 是否超过宽度限制
  if (!H && !Q)                    // 如果都不超限
    return {text: A, isTruncated: !1};   // ← 返回原文，不截断
  // ... 截断逻辑 ...
  return {text: J, isTruncated: !0};     // ← 返回截断后的文本
}
```

**修改**: `if(!H&&!Q)` → `if(!0||!Q)`

```plain
原: if(!H && !Q)  → 只有当 H=false 且 Q=false 时才返回原文
改: if(!0 || !Q)  → !0 是 true，所以 true || 任何 = true，永远返回原文
```

**效果**:

- 永远走早期返回分支，返回原文 + `isTruncated:!1`（不显示 Ctrl+O 提示）
- 后面的截断逻辑永远不执行
- 因此原来的"截断参数 R=80,T=3"和"截断返回 isTruncated:!0"修改都不需要了

### 修改 4: diff/edit 显示行数

**位置**: `iTT()` 函数的默认行数参数

**原始代码**:
```javascript
function iTT(H, T=iIq, R=dIq) {
  if (!H) return H;
  let A = H.split("\n");
  if (A.length > T) D = A.slice(0, T) // 截断到 T 行
  ...
  C += "\n... [truncated]";
}
var iIq=20, dIq=2000;  // 20行, 2000字符
```

**修改**: `var iIq=20,dIq=2000` → `var iIq=99,dIq=2000`

**锚点**: `var V=20,V=2000` 模式唯一（伴生变量 dIq=2000 提供确定性定位）

- 原来 diff/输出最多显示 20 行
- 现在显示 99 行

## 修改汇总

| #   | 修改项       | 原始         | 修改后         | 字节 | 说明                                      |
| --- | ------------ | ------------ | -------------- | ---- | ----------------------------------------- |
| 1   | 截断条件     | `if(!H&&!Q)` | `if(!0\|\|!Q)` | 0    | 短路截断函数，隐藏命令框 "press Ctrl+O"   |
| 4   | diff 行数    | `iIq=20`     | `iIq=99`       | 0    | Edit diff/输出显示 99 行                  |
| 6   | model cycle  | peek/cycle 函数 | 覆盖H+`/\[/`过滤 | ~+24 | Ctrl+N 跳过 Copilot model (ID 含 `[` 的模型) |
| 7   | 多行历史     | `V(),!0`     | `(spaces)!1`   | 0    | 多行历史按↓可返回空输入框             |
| 8   | Welcome 橙色 | 多处 Text 属性 | +`color:"#FFA500"` + Header "Modified" | ~+63 | 欢迎文字橙色 + 版本号加 Modified |
| 9   | effort 级别  | `["off","low","medium","high"]` | 追加 `"max"` | +12 | wUT() 自动映射 openai "xhigh" |
| 10  | kitty 超时   | `setTimeout(B,200)` | `setTimeout(B,999)` | 0 | 缓解 iTerm2 kitty 协议竞态条件 |
| 补偿 | 死代码区域   | 多处死代码   | 注释/缩短填充   | ~-84 | 统一补偿 mod6(~+27) + mod8(+45) + mod9(+12) |

**注**：
- mod1: 命令框提示（command truncated）
- mod6: 修改 `peekNextCycleModel`, `peekNextCycleSpecModeModel`, `cycleSpecModeModel` 三个函数
  （`cycleModel` 是委托函数，无需修改；覆盖参数为 customModels ID，用 `/\[/.test()` 跳过 Copilot）
- mod7: `_T` 函数中 `onDownArrowAtBottom` 返回值修复
- mod8: `Ij` 函数中多处 Text 元素添加 #FFA500 hex color，版本号追加 " Modified"
- mod9: 在 effort 数组追加 "max"，wUT() 内置 "max"→"xhigh" 映射处理 openai
- mod10: `confirmKittySupport` 中 `setTimeout` 超时从 200ms 增至 999ms

### 修改 7: 多行历史记录按↓修复

**位置**: `_T` 函数（光标在多行文本内移动）

**问题**: 多行文本最后一行按 ↓ 时，`_T` 调用 `onDownArrowAtBottom` 并返回 `true`，导致外层 handler 跳过 `navigateNext()` 历史导航。

**修改**: `V(),!0` → `(spaces)!1`

```plain
原: if(EH)return EH(),!0}return!1
改: if(EH)return      !1}return!1
```

**效果**: `_T` 返回 `false`，外层 handler 执行 `navigateNext()` 回到空输入框。

### 修改 8: Welcome/Header 橙色 + "Modified" 标记

**位置**: 两个渲染路径

1. `rID` 函数 (旧 Welcome 页面，JSX 渲染): 多处 Text 元素添加 `color:"#FFA500"`，版本号追加 " Modified"
2. Header 函数 (新 canvas header，`Ib` 绘制): 版本号文本追加 " Modified"

**路径1 (rID)**:

| 元素 | 原始 | 修改后 | 字节 |
|------|------|--------|------|
| Logo | `{bold:!0,children:A}` | `{bold:!0,color:"#FFA500",children:A}` | +16 |
| 版本 | `{dimColor:!0,children:"vX.Y.Z"}` | `{color:"#FFA500",children:"vX.Y.Z Modified"}` | +13 |
| 标语 | `{italic:!0,children:VAR}` | `{italic:!0,color:"#FFA500",children:VAR}` | +16 |

**路径2 (Header)**:

```javascript
// 原始:
Ib(E,j,V("v0.89.0"),"v0.89.0","dim-bold")
// 修改:
Ib(E,j,V("v0.89.0 Modified"),"v0.89.0 Modified","dim-bold")
```

+18 bytes (两处 `" Modified"` 各 +9)

**效果**: Welcome 和 Header 页面版本号后均带 "Modified" 标记，Welcome 文字橙色。

**稳定锚点**:
- 路径1: `dimColor:!0,children:"v` + 版本号正则
- 路径2: `V("vX.Y.Z"),"vX.Y.Z","dim-bold")` — 唯一模式

### 修改 6: Ctrl+N 只在 custom model 间切换（容错版）

**目标函数**: `peekNextCycleModel`, `peekNextCycleSpecModeModel`, `cycleSpecModeModel` (3 个)

> `cycleModel` 是委托函数（调用 `peekNextCycleModel`），无 `validateModelAccess`，无需修改。

使用 `_find_at_or_near` 容错定位（偏移有变化时在 ±64 字节窗口内搜索），
通过 `early_return` 参数适配不同函数的返回值（`null` vs `this.getSpecModeModel()`），
支持双参数 `fn(H,A)` 签名。

**原始代码** (以 peekNextCycleModel 为例):

```javascript
peekNextCycleModel(H){
  if(H.length===0)return null;
  ...
  if(!this.validateModelAccess(D).allowed)continue;
  ...
}
```

**修改**:
1. 函数入口覆盖参数: `H=this.customModels.map(m=>m.id);` (+33 bytes)
2. `validateModelAccess` 检查替换为 `/\[/.test(VAR)` copilot 过滤 (~-25 bytes vs -50 bytes)
3. 剩余空间用注释填充或接受字节增长

```javascript
peekNextCycleModel(H){
  H=this.customModels.map(m=>m.id);
  if(H.length===0)return null;
  ...
  if(/\[/.test(D))continue;
  ...
}
```

**效果**: Ctrl+N 只在 settings.json 中配置的非 Copilot custom model 间切换
（ID 含 `[` 的模型被跳过，如 `custom:[CopilotFree]-...` 和 `custom:[CopilotPay]-...`），
`/model` 菜单不受影响

**字节**: 每个函数约 +8 bytes（注入 +33, 检查替换 25B vs 原 50B），总计约 +24 bytes

**稳定锚点**（不受混淆影响）:
- `peekNextCycleModel` / `peekNextCycleSpecModeModel` / `cycleSpecModeModel` — 方法名
- `this.validateModelAccess` / `.allowed` — 方法和属性名
- `this.customModels` — 属性名

### 修改 9: Custom model 完整 effort 级别

**位置**: custom model 配置构建处（2 处）

**问题**: custom model 硬编码 `supportedReasoningEfforts` 为 `["off","low","medium","high"]`，
缺少最高级 `"max"`，导致 Tab 切换无法到达该级别。

**原始代码**:
```javascript
supportedReasoningEfforts:L?["off","low","medium","high"]:["none"]
```

**修改**:
```javascript
supportedReasoningEfforts:L?["off","low","medium","high","max"]:["none"]
```

**效果**:
- 所有 custom model: `off → low → medium → high → max → off ...`
- OpenAI 由 `wUT()` 内置映射自动将 `"max"` → `"xhigh"` 发送到 API

**字节**: +6 bytes/处，共 2 处 = +12 bytes，由 `comp_universal.py` 统一补偿。

**稳定锚点**: `supportedReasoningEfforts`、`["off","low","medium","high"]` — 字符串常量。

**配合 mod9**: 应用 mod9 后，检查 `~/.factory/settings.json` 中 `extraArgs` 的 effort 相关参数。
mod9 解锁了完整 effort 级别后，extraArgs 中的 effort 参数已冗余，且会导致副作用。

**交互流程**:
1. 运行 `status.py` 检查配置
2. 如果发现 extraArgs 中有 effort 相关参数，询问用户是否移除，并说明：
   - Anthropic: `extraArgs.thinking` 和 `extraArgs.output_config.effort` 已不需要
   - OpenAI: 必须移除整个 `extraArgs.reasoning` 对象（包括 `reasoning.summary`），`text.verbosity` 可保留
   - **不移除的后果**:
     - `extraArgs` 在 `responses.create()` 中通过 JS 浅展开 (`...extraArgs`) 排在 `requestParams` 之后
     - `extraArgs.reasoning` 会整个覆盖 `requestParams.reasoning`（含 `effort` 字段），导致 effort 丢失
     - 结果：Tab 切换 Thinking Level 完全无效
3. 用户确认后修改 settings.json

### 修改 10: Kitty keyboard 检测超时

**位置**: `confirmKittySupport` 函数中的 `setTimeout`

**问题**: 在 iTerm2 上，kitty keyboard protocol 查询 (`\x1B[?u`) 的响应有时在 Ink/React 的 stdin 监听器就绪后才到达，导致响应被 React 消费而非 kitty 检测代码。泄漏到屏幕的 `^[[?0u` 和 `^[[?64;...c` 就是这些未被正确处理的终端响应。

**修改**: `setTimeout(B,200)` → `setTimeout(B,999)`

- 200ms → 999ms，给终端更多时间响应
- 0 字节变化（`200` 和 `999` 都是 3 字符）
- 仅影响不支持 kitty 协议的终端的启动时间（多等 ~0.8s）
- 支持 kitty 协议的终端响应通常几毫秒内返回，不受影响

**稳定锚点**: `enableKittyProtocol` — 在 `setTimeout` 后 100 字节内出现。

## 修改脚本

脚本位置: `~/.factory/skills/droid-bin-mod/scripts/`

### mods/ - 功能修改

```bash
mods/mod1_truncate_condition.py  # 截断条件短路 (0 bytes)
mods/mod4_diff_lines.py          # diff行数 20→99 (0 bytes)
mods/mod6_custom_model_cycle.py  # Ctrl+N 跳过 Copilot model (~+27 bytes)
mods/mod7_multiline_history.py   # 多行历史↓键修复 (0 bytes)
mods/mod8_welcome_modified.py    # Welcome 橙色 + Modified 标记 (+45 bytes)
mods/mod9_custom_effort_levels.py # custom model effort 级别 (+12 bytes)
mods/mod10_kitty_timeout.py      # kitty 检测超时 200→999ms (0 bytes)
```

mod6 产生 ~+27 bytes，mod8 产生 +45 bytes，mod9 产生 +12 bytes。
由 `comp_universal.py` 统一补偿（实际字节数以各 mod 输出之和为准）。

### compensations/ - 字节补偿

```bash
compensations/comp_universal.py          # 通用补偿，利用所有 mod 的死代码区域 (~187B 可用)
compensations/comp_universal.py          # 无参数: 显示当前可用补偿空间
compensations/comp_universal.py <bytes>  # 缩减指定字节数
compensations/comp_substring.py <bytes>  # 旧方案：仅修改 FFH 函数的 substring
compensations/comp_r80_to_r8.py          # 旧方案：R=80→R=8 (-1 byte)
```

用法：`python3 comp_universal.py N` 补偿所有 mod 的总字节增量（N = mod6 + mod8 + mod9 的实际输出之和，v0.73+ 模式下 mod3 为 0）。

补偿区域来源 (由各 mod 短路/替换产生的死代码):
- FFH 死代码 (mod1 短路): ~137B — 截断函数被短路后的不可达代码，替换为 `;return{text:H,isTruncated:!1}`

### 执行示例（跨平台）

```bash
# 1. macOS: 移除签名
[[ "$OSTYPE" == "darwin"* ]] && codesign --remove-signature ~/.local/bin/droid

# 2. 执行修改
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod1_truncate_condition.py
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod4_diff_lines.py
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod6_custom_model_cycle.py  # ~+24 bytes
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod7_multiline_history.py
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod8_welcome_modified.py      # +45 bytes
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod9_custom_effort_levels.py  # +12 bytes
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod10_kitty_timeout.py       # 0 bytes
python3 ~/.factory/skills/droid-bin-mod/scripts/compensations/comp_universal.py 84  # 补偿 mod6(~+27) + mod8(+45) + mod9(+12)

# 3. macOS: 重新签名
[[ "$OSTYPE" == "darwin"* ]] && codesign -s - ~/.local/bin/droid
```

**说明**：`[[ "$OSTYPE" == "darwin"* ]]` 自动检测平台，macOS 执行签名操作，Linux 跳过。

### 工具脚本

```bash
python3 ~/.factory/skills/droid-bin-mod/scripts/status.py   # 检查状态
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py  # 恢复原版
```

脚本使用正则匹配变量名，适应混淆后变量名变化。

## 前提条件

- macOS 或 Linux 系统
- Python 3
- droid 二进制位于 `~/.local/bin/droid`

**平台差异**：
- macOS: 需要 codesign 移除/重签签名
- Linux: 无需签名操作，直接修改即可
- Windows: 未测试，不支持

## 修改流程（跨平台）

```bash
# 1. 备份 (带版本号)
cp ~/.local/bin/droid ~/.local/bin/droid.backup.$(~/.local/bin/droid --version)

# 2. macOS: 移除签名
[[ "$OSTYPE" == "darwin"* ]] && codesign --remove-signature ~/.local/bin/droid

# 3. 执行修改脚本 (参考上面的修改原理)

# 4. macOS: 重新签名
[[ "$OSTYPE" == "darwin"* ]] && codesign -s - ~/.local/bin/droid

# 5. 验证
~/.local/bin/droid --version
```

## 测试修改效果

修改完成后，告诉用户：

```plain
新开一个 droid 窗口，输入"测试droid修改"
```

### 测试命令（供 droid 执行）

```bash
# 测试修改1 (命令截断)
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" && echo done

# 测试修改4 (diff行数) - 先创建文件
seq 1 100 > /tmp/test100.txt
# 然后让 droid 编辑前30行看 diff
```

### 检查点

- 修改 1: 命令框不再显示 "command truncated. press Ctrl+O for detailed view"
- 修改 4: diff 显示超过 20 行（原来只显示 20 行）

## 恢复原版

**推荐用脚本恢复**（macOS 上直接 cp 会因元数据问题导致 SIGKILL，Linux 可直接 cp）：

```bash
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py --list  # 查看备份
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py         # 恢复最新
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py 0.46.0  # 恢复指定版本
```

## 禁用自动更新

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export DROID_DISABLE_AUTO_UPDATE=1
```

## 安全说明

- 此修改仅影响本地 UI 渲染
- Factory 服务器不验证客户端二进制完整性
- 不发送二进制哈希、签名、机器指纹
- 只验证 API Key 有效性

## 版本升级后脚本失败的排查

如果 droid 更新后脚本报错"未找到"，按以下步骤排查：

### 1. 检查特征数字是否变化

```bash
# 这些数字有语义含义，通常不会变
strings ~/.local/bin/droid | grep -E "=80,|=3\)|=20,"
```

- `80` - 截断宽度限制
- `3` - 截断行数限制
- `20` - diff 显示行数

### 2. 检查字符串常量是否存在

```bash
strings ~/.local/bin/droid | grep -E "isTruncated|=2000"
```

### 3. 更新脚本正则

如果变量名模式变化（如单字母→多字母），修改 `common.py` 中的 `V` 模式：

```python
# 当前模式 (适应大多数混淆器)
V = rb'[A-Za-z_$][A-Za-z0-9_$]*'
```

### 4. 重新备份

```bash
cp ~/.local/bin/droid ~/.local/bin/droid.backup.$(~/.local/bin/droid --version)
```

### 5. mod4/6/7/8/9/10 排查

**mod4** (diff行数):
```bash
strings ~/.local/bin/droid | grep -E "var [A-Za-z_$]+=20,[A-Za-z_$]+=2000"
```

**mod6** (custom model cycle):
```bash
strings ~/.local/bin/droid | grep -E "peekNextCycleModel|cycleSpecModeModel|validateModelAccess"
```

**mod7** (多行历史):
```bash
# 检查 _T 函数中 onDownArrowAtBottom 返回值
strings ~/.local/bin/droid | grep -c "return!1}return!1"
```

**mod8** (Welcome 橙色):
```bash
strings ~/.local/bin/droid | grep "FFA500"
strings ~/.local/bin/droid | grep "Modified"
```

**mod9** (effort 级别):
```bash
strings ~/.local/bin/droid | grep "supportedReasoningEfforts"
strings ~/.local/bin/droid | grep -E '\["off","low","medium","high"\]'
```

**mod10** (kitty 超时):
```bash
strings ~/.local/bin/droid | grep "enableKittyProtocol"
strings ~/.local/bin/droid | grep -E "setTimeout\([A-Za-z],200\)"
```
