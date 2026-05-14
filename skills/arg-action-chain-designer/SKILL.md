---
name: arg-action-chain-designer
version: "1.1.1"
description: Use this skill when the user wants to create, refine, review, or convert an agent task or existing skill into an ARG Action Chain / ARG 行动链路. This skill is especially relevant for recurring automations, multi-step agent jobs, data pipelines, report generation, MCP workflows, or tasks where agent drift, hallucinated fields, self-verification, premature planning, or uncontrolled long-context execution are risks. Trigger when the user mentions ARG, Step Contract, clue card, validation gate, progressive disclosure, reducing agent drift/self-deception, converting a normal skill into arg-xxx, or making a task chain more bounded and verifiable.
---

# ARG Action Chain Designer

## 目标

把一个模糊的 Agent 任务、已有 skill，或需要重复执行的工作流，设计成可复用的 ARG 行动链路。

这里的默认架构叫 **Static Progressive Clue Chain / 静态渐进线索链**：执行 Agent 运行时只看到当前 Step Contract，完成当前任务，通过验证门禁后，才解锁下一张线索卡。

这个 skill 不应该只给一段建议就结束。默认先产出可落地的设计；当用户需要文件级交付物时，继续生成薄 `SKILL.md` 引擎、`plans/step-*.md`、必要的 `scripts/` 草案。若用户已经明确说“创建、生成、写入、落地、打包”，且当前工作区可写，就直接生成文件。

## 默认架构：静态渐进线索链

默认使用这套运行模型：

```text
薄 SKILL.md 引擎
  -> 只读取当前 plans/step-NN-name.md
  -> 执行当前任务
  -> 在 output/ 里产出结构化结果
  -> 执行当前 step 的验证命令
  -> 验证通过后，读取当前 step 末尾的【下一步】
  -> 重复，直到 TERMINAL
```

术语含义：

- `Static / 静态`：线索卡预先存在，执行 Agent 不临场发明路线。
- `Progressive / 渐进`：运行时逐步揭示，Agent 只能读当前 step。
- `Clue Chain / 线索链`：每个 `plans/step-*.md` 都是一张 Step Contract，验证通过才解锁下一张。
- 上一步的输出，是下一步的输入。
- 验收权威来自验证命令、脚本、schema、断言或人工门禁，不来自 Agent 的自我声明。

默认不要设计持久化进度文件。可运行链路每次都从 skill 引擎入口开始。只有用户明确要求“断点续跑、可恢复、长周期任务恢复”时，才额外设计状态机制，而且必须避免执行 Agent 通过编辑状态来伪造完成。

## 标准交付结构

生成可运行 ARG skill 时，默认使用这个结构：

```text
arg-name/
├── SKILL.md
├── plans/
│   ├── step-00-start.md
│   ├── step-01-fetch.md
│   ├── step-02-process.md
│   └── step-NN-final.md
├── scripts/
│   ├── extract_for_judgment.*
│   ├── merge_or_transform.*
│   └── validate_*.*
└── output/
```

`SKILL.md` 必须薄。业务细节放进 `plans/`，确定性处理放进 `scripts/`，运行产物放进 `output/`。

## 核心立场

把执行 Agent 当成“能力强，但不可信”的玩家。

- Agent 是玩家，不是出题人。
- Step Contract 是最小行动边界。
- 执行时不要让 Agent 看到完整地图。
- 验证门禁是验收，不是建议。
- LLM 判断必须被限制在字段、枚举、例子、schema 或人工门禁里。
- raw/source 原始数据应由脚本保留和合并，不交给 Agent 自由改写。
- 确定性工作交给脚本、验证器或窄命令。
- 外部发送、不可逆动作、高风险业务判断、主观质量判断，需要人工门禁或明确外部门禁。

如果 ARG 对任务来说过度设计，或任务根本无法验证，要直接说明，并建议更简单的模式。

## 适配判断

多数条件成立时，推荐 ARG：

- 任务有多个步骤。
- 任务会重复执行，或需要稳定执行。
- 每一步都能产出具体文件、对象、状态或可观察结果。
- 每个产物都能被命令、schema、断言、清单或人工门禁检查。
- LLM 只在有限字段里做语义判断。
- 失败处理很重要。

以下任务不适合优先用 ARG：

- 开放式研究。
- 头脑风暴或策略讨论。
- 高度交互式对话。
- 纯主观创作。
- 单步查询。
- 必须让 Agent 在执行中自由探索路线的任务。

可替代方案包括：纯脚本、普通 skill、ReAct、plan-and-execute、DAG 工作流、人机协作，或带人工门禁的 ARG。

## 工作流程

### 1. 理解任务

先从用户请求和仓库上下文里推断已知信息。只有在不问就会假装确定时，才最多问一个关键问题。能安全假设时，带着明确假设继续。

需要捕获：

- 最终产物。
- 输入来源：文件、API、用户上下文、凭据、定时任务、外部系统。
- 可脚本化部分：命令、转换、验证、合并。
- LLM 判断边界：哪些字段必须靠模型判断。
- 验证策略：每个结果怎么检查。
- 失败策略：重试、跳过、降级、停止、人工复核。
- 交付意图：只要设计，还是需要文件级链路包。

### 2. 给出结论

先明确结论：

- `适合 ARG`
- `适合 ARG，但需要人工门禁`
- `不适合 ARG`
- `先用普通 skill，后续再 ARG 化`

然后继续给出设计，不要停在泛泛建议。

### 3. 设计链路

输出：

- 任务边界。
- 链路草图。
- Step Contracts。
- 验证门禁。
- 失败处理。
- 运行 skill 骨架。
- 风险和补强。

如果链路需要初始化、清理或环境检查，用 `step-00-*` 作为入口。最后一步的【下一步】必须是 `TERMINAL`。

### 4. 询问是否落成文件

完成诊断和链路草图后，询问一次用户是否需要文件级交付物。若用户已经明确要求“创建、写入、生成、落地、打包”，不要再问，直接做。

推荐话术：

```text
我可以继续把它落成文件级交付物：
- `SKILL.md` 薄运行引擎
- `plans/step-*.md` Step Contracts
- 必要的 `scripts/validate_*.py` / transform scripts 草案

如果你要，我下一步直接生成这些文件。
```

如果用户确认且工作区可写，直接创建或修改文件。若不可写，输出完整文件内容和建议路径。

## 转换已有 skill 的规则

当用户要把已有 skill ARG 化：

- 默认不覆盖原 skill。
- 原 skill 名为 `foo` 时，新 skill 默认命名为 `arg-foo`。
- 原 skill 只作为素材读取，再围绕静态渐进线索链设计新的 ARG runtime。
- 只有用户明确说“覆盖原 skill / 直接改原 skill / 替换原 skill”时，才允许编辑原 skill。
- 不要在新 runtime `SKILL.md` 里写 `Derived from foo` 之类来源说明；这会干扰执行 Agent。需要记录来源时，只写在最终报告或外部说明里。
- 保留原 skill 的有用领域能力，但把业务步骤移入 `plans/`，让新的 `SKILL.md` 保持薄引擎。

如果用户是从新需求出发，而不是从已有 skill 出发，选择清晰的 `arg-*` 名称，例如 `arg-report-reviewer`、`arg-data-cleanup-chain`。

## Step Contract 标准

每个 `plans/step-NN-name.md` 必须自包含，并包含以下 section：

```md
# Step NN: [Name]

## 输入
[明确文件、API、用户上下文，或写“无”]

## 任务
[命令或受限语义指令；一个 step 只做一类工作]

## 输出
[精确产物路径、对象结构、状态文件或可见结果]

## 验证命令
[可执行命令、schema 检查、断言、清单或人工门禁]

## 验证失败处理
[重试次数、跳过/降级/停止/人工复核，以及失败记录位置]

## 下一步
`plans/step-NN-next.md` 或 `TERMINAL`
```

如果一个 step 同时抓取、分类、渲染、通知，应该拆开。大型渲染 step 可以内部拆成多个 block，但每个 block 都要有验证，通过后才能继续。

## 薄 SKILL.md 运行模板

生成可运行 ARG skill 时，使用下面的模板，并按用户环境替换名称和路径。

````md
---
name: arg-name
description: Only use this skill when the user explicitly invokes /arg-name or clearly asks to run this ARG chain. Executes [domain] through a static progressive clue chain with validation gates.
allowed-tools: Bash
---

# arg-name

## 触发方式

仅接受显式命令触发：`/arg-name`

不要从普通自然语言问题中猜测触发，除非用户明确要求执行这条链。

```text
设 OUTPUT_DIR = "[absolute-or-project output path]"
设 PLANS_DIR = "[absolute-or-project plans path]"
设 SCRIPTS_DIR = "[absolute-or-project scripts path]"
设 "当前步" = "step-00-start"

循环：
1. 读取 PLANS_DIR/当前步.md
2. 严格按文件中的【任务】说明执行
3. 执行文件中的【验证命令】
4. 验证通过 → 读取文件末尾【下一步】，赋值给当前步
5. 验证失败 → 按文件中的【验证失败处理】执行
6. 当前步 = "TERMINAL" → 退出循环，输出执行汇报
```

起始：读取 `PLANS_DIR/step-00-start.md`。

## 关键原则

1. **逐步揭示**：你只知道当前这一步。每步末尾的【下一步】会告诉你该读哪个文件。不要推测或预判后续步骤。
2. **验证门禁**：每步必须通过验证命令才能进入下一步。验证失败必须按失败处理执行。
3. **字段受限**：当步骤要求你填写判断字段时，只填写被授权字段，不能修改 raw/source 字段。
4. **路径稳定**：命令使用约定的 OUTPUT_DIR/PLANS_DIR/SCRIPTS_DIR，不依赖未知工作目录。
5. **不得自证**：不能用“我检查过了”代替验证命令或人工门禁。
````

runtime `SKILL.md` 不应在引擎之外写完整业务地图。业务地图存在 step 文件中，并在运行时逐步揭示。

## LLM 判断装盒

当某一步需要语义判断时，让 Agent 只填写小型结构化产物：

```json
[
  {
    "index": 0,
    "relevant": "yes",
    "summary": "中文概括，不超过 60 字",
    "sentiment": "正向",
    "date_iso": "2026-05-06 14:30"
  }
]
```

规则：

- 在 step 内定义枚举值。
- 容易混淆的标签要给边界例子。
- 用 extractor script 只提取判断所需字段。
- 用 merge script 从 raw/source 复制原始字段，只合并被授权的判断字段。
- 验证 counts、必填字段、枚举、日期格式、占位符泄漏、raw 字段保护。

## 验证门禁设计

优先使用硬验证：

- 文件存在且非空。
- JSON/YAML 可解析。
- schema 匹配。
- `total == len(items)` 或同类数量一致性。
- 枚举值合法。
- 必填字段非空。
- 没有占位符泄漏。
- raw/source 字段未被改写。
- 渲染结果包含必需 section，且不含禁止结构。
- 外部动作有明确成功证据。

只有硬验证不可行时，才使用软检查。外部发送、不可逆动作、合规敏感判断、主观质量判断，使用人工门禁。

不要接受“Agent 应该仔细检查”作为唯一验证。

## 失败处理标准

每一步都要写清楚具体策略：

- 硬失败：停止或进入人工复核。
- 软失败：有限次数重试。
- 部分失败：跳过或降级，并记录状态。
- 验证失败：只重新生成被授权的输出，再重新验证。
- 外部动作失败：不要盲目重试，必须考虑幂等性或人工确认。

始终写清楚重试次数和停止条件。

## 复查清单

最终定稿前检查：

- runtime `SKILL.md` 是否足够薄。
- 业务细节是否都在 `plans/`，而不是塞在引擎里。
- 每个 step 是否都有 输入 / 任务 / 输出 / 验证命令 / 验证失败处理 / 下一步。
- 每个 step 是否只做一类工作。
- 验证是否检查结构和内容，而不是只检查文件存在。
- raw/source 字段是否被保护，避免 Agent 改写。
- LLM 判断是否被限制在枚举、小摘要和授权字段里。
- 失败策略是否有边界。
- 是否存在 `TERMINAL`。
- 是否写明隐藏依赖：cwd、凭据、当前时间、登录态、外部工具、定时任务。
- 不可逆动作是否有人工或外部门禁。
- 执行 Agent 是否避免读取未来 step。

## 输出模式

### 模式 A：设计新 ARG 链路

用户要求设计、构建或转换任务时使用。

输出：

```md
## 结论
适合 ARG / 适合 ARG 但需要人工门禁 / 不适合 ARG

## 任务边界
- 最终产物：
- 输入来源：
- Agent 可判断：
- 必须脚本化：
- 验收权威：

## 架构
Static Progressive Clue Chain / 静态渐进线索链

## 链路草图
step-00-start -> step-01-name -> step-02-name -> TERMINAL

## Step Contracts
### step-00-start
- 输入：
- 任务：
- 输出：
- 验证命令：
- 验证失败处理：
- 下一步：

## 运行 Skill 骨架
- 触发方式：
- OUTPUT_DIR：
- PLANS_DIR：
- SCRIPTS_DIR：
- 当前步：
- 禁止行为：

## 风险和补强
- ...

## 文件级交付物
询问用户是否需要继续生成 `SKILL.md`、`plans/step-*.md`、必要 scripts。
```

### 模式 B：诊断已有链路

用户提供 skill、plan、chain 或 Step Contract，并询问是否合理时使用。

输出：

```md
## 结论
可用 / 需补强 / 风险较高

## 主要缺口
- ...

## 逐步诊断
| Step | 问题 | 建议 |
| --- | --- | --- |

## 必须补的 ARG 细节
- ...

## 可以暂缓的改进
- ...
```

### 模式 C：把已有 skill 转成 arg-xxx

用户要优化或转换已有 skill 时使用。

输出：

```md
## 转换策略
- 原 skill：
- 新 skill：
- 是否覆盖原 skill：否，除非用户明确要求

## 保留能力
- ...

## ARG 化改造
- 薄 `SKILL.md` 引擎：
- `plans/` Step Contracts：
- `scripts/` 确定性处理：
- `output/` 产物：

## 下一步
询问是否生成文件级 `arg-xxx` 交付物；若用户已要求生成，则直接创建。
```

### 模式 D：把模糊想法变成需求

用户只有一个想法，还没有清晰任务时使用。

输出紧凑需求草案：

```md
## ARG 需求草案
- 目标：
- 最终产物：
- 输入：
- 不确定点：
- 可脚本化部分：
- 需要 LLM 判断的部分：
- 验证策略：
- 失败策略：

## 最小链路草图
step-00-start -> step-01-name -> TERMINAL

## 需要确认的一问
...
```

## 最终回复标准

结尾要给具体下一步。

设计类请求：询问是否继续生成文件级交付物。

生成类请求：报告创建/修改了哪些文件，以及做过什么验证。

好的结尾：

```text
我可以继续把它落成 `arg-competitor-monitor/`：薄 `SKILL.md`、4 个 step contracts、2 个验证脚本。你确认要文件级交付物的话，我下一步直接生成。
```

生成文件后的结尾：

```text
已生成 `skills/arg-foo/`。关键文件是 `SKILL.md`、`plans/step-00-start.md`、`plans/step-01-fetch.md`、`scripts/validate_step_01.py`。已检查每个 step 都包含六个必需 section，且终点为 `TERMINAL`。
```

不好的结尾：

```text
我们应该持续优化 agent 的可靠性。
```
