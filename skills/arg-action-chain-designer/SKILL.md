---
name: arg-action-chain-designer
version: "1.1.0"
description: Use this skill when the user wants to create, refine, review, or convert an agent task or existing skill into an ARG Action Chain / ARG 行动链路. This skill is especially relevant for recurring automations, multi-step agent jobs, data pipelines, report generation, MCP workflows, or tasks where agent drift, hallucinated fields, self-verification, premature planning, or uncontrolled long-context execution are risks. Trigger when the user mentions ARG, Step Contract, clue card, validation gate, progressive disclosure, reducing agent drift/self-deception, converting a normal skill into arg-xxx, or making a task chain more bounded and verifiable.
---

# ARG Action Chain Designer

## Mission

Turn a vague agent task, existing skill, or repeated workflow into a reusable ARG Action Chain: a static progressive clue chain where the runtime agent sees only the current Step Contract, executes it, passes validation, then unlocks the next clue.

The default goal is not to give advice and stop. Produce a usable design first, then explicitly ask whether the user wants a file-level deliverable. If the user already asks to create, generate, write, land, or package the chain, create the deliverable directly when the workspace is writable.

## Core Model: Static Progressive Clue Chain

Use this as the default architecture.

```text
thin SKILL.md engine
  -> read only current plans/step-NN-name.md
  -> execute current task
  -> produce structured artifacts in output/
  -> run the step validation command
  -> if validation passes, read the current step's 下一步 field
  -> repeat until TERMINAL
```

Meaning:

- `Static`: clue cards exist before runtime. The executing agent does not invent the route.
- `Progressive`: only the current clue card is visible during execution.
- `Clue Chain`: each `plans/step-*.md` is a Step Contract unlocked by validation.
- Previous step outputs become the next step inputs.
- Verification gates, scripts, schemas, or human gates are the acceptance authority, not the agent's self-report.

Do not default to persistent progress files. A runnable chain starts from the skill engine each time. Add resumable state only when the user explicitly asks for 断点续跑 / resumability / long-cycle recovery, and then design it so the executing agent cannot forge completion by editing state.

## Proven Runtime Shape

When producing a runnable ARG skill, mirror this shape:

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

Keep `SKILL.md` thin. Business details belong in `plans/`. Deterministic work belongs in `scripts/`. Runtime artifacts belong in `output/`.

## Core Stance

Treat the executing agent as capable but untrusted.

- The agent is the player, not the puzzle designer.
- The Step Contract is the smallest action boundary.
- The agent must not see the full map while executing.
- Validation is the gate, not a suggestion.
- LLM judgment must be boxed into fields, enums, examples, schemas, and merge scripts.
- Raw source data should be preserved by scripts, not rewritten by the agent.
- Deterministic work belongs in scripts, validators, or narrow commands.
- Human gates are required for irreversible actions, external sends, sensitive business judgment, or subjective approval.

If ARG is overkill or the task cannot be validated, say so directly and suggest a simpler pattern.

## Fit Decision

Recommend ARG when most are true:

- The task has multiple steps.
- The task repeats or needs stable execution.
- Each step can produce a concrete artifact or observable state.
- Each artifact can be checked by a command, schema, assertion, checklist, or human gate.
- LLM judgment is needed only in bounded places.
- Failure behavior matters.

Do not use ARG as the primary pattern when the task is:

- Open-ended research.
- Brainstorming or strategy discussion.
- Highly interactive conversation.
- Purely subjective creation.
- A one-step query.
- A task where the agent must freely discover the path during execution.

Better alternatives may be: pure script, regular skill, ReAct, plan-and-execute, DAG workflow, human collaboration, or ARG with explicit human gates.

## Workflow

### 1. Understand The Task

Infer what is already known from the user request and repository context. Ask at most one critical question if proceeding would otherwise fake certainty. Prefer explicit assumptions when safe.

Capture:

- Final artifact.
- Inputs: files, APIs, user context, credentials, schedule, external systems.
- Deterministic work: scripts, commands, transforms, validation.
- LLM judgment: exactly which fields require semantic judgment.
- Validation: how each result is checked.
- Failure policy: retry, skip, degrade, stop, or human review.
- Delivery intent: design-only or file-level chain package.

### 2. Choose The Outcome

State one clear decision:

- `适合 ARG`
- `适合 ARG，但需要人工门禁`
- `不适合 ARG`
- `先用普通 skill，后续再 ARG 化`

Then produce the design. Do not stop at a generic recommendation.

### 3. Design The Chain

Produce:

- Task boundary.
- Chain sketch.
- Step Contracts.
- Validation gates.
- Failure policy.
- Runtime skill skeleton.
- Risks and补强.

Use `step-00-*` for setup/cleanup/entry when the chain has a real runtime initialization step. Use `TERMINAL` as the final next marker.

### 4. Offer File-Level Delivery

After the design is clear, ask once whether the user wants the file-level deliverable, unless they already asked to create/write/generate/land/package it.

Use wording like:

```text
我可以继续把它落成文件级交付物：
- `SKILL.md` 薄运行引擎
- `plans/step-*.md` Step Contracts
- 必要的 `scripts/validate_*.py` / transform scripts 草案

如果你要，我下一步直接生成这些文件。
```

If the user confirms and the workspace is writable, create or modify files. If not writable, output complete file contents and recommended paths.

## Existing Skill Conversion Rules

When the user wants to ARG-wrap an existing skill:

- Do not overwrite the original skill by default.
- If the original skill is named `foo`, create a new skill named `arg-foo`.
- Read the original skill as source material, then design the new ARG runtime around the static progressive clue chain.
- Only edit or replace the original skill if the user explicitly says to overwrite it.
- Do not write "Derived from foo" or similar provenance inside the generated runtime `SKILL.md`; it can confuse the executing agent. Mention provenance only in the final report or external notes if useful.
- Preserve the original skill's useful domain behavior, but move business steps into `plans/` and keep the new `SKILL.md` as a thin engine.

When the user starts from a new requirement rather than an existing skill, choose a descriptive name such as `arg-report-reviewer`, `arg-data-cleanup-chain`, or another domain-specific `arg-*` name.

## Step Contract Standard

Each `plans/step-NN-name.md` must be self-contained and include these sections:

```md
# Step NN: [Name]

## 输入
[Explicit files, APIs, user-provided context, or "无"]

## 任务
[Commands or bounded semantic instructions. One kind of work only.]

## 输出
[Exact artifact paths, object shape, status file, or visible result]

## 验证命令
[Executable command, schema check, assertion, checklist, or human gate]

## 验证失败处理
[Retry limit, skip/degrade/stop/human review, and where failure is recorded]

## 下一步
`plans/step-NN-next.md` or `TERMINAL`
```

Split a step when it fetches, classifies, renders, and notifies at once. A large render step may contain internal blocks only when each block has its own validation before continuing.

## Thin Runtime SKILL.md Template

Use this pattern when generating a runnable ARG skill. Adapt names and paths to the user's environment.

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

The runtime `SKILL.md` must not include the full business map outside the engine. The map lives in the step files and is revealed one step at a time.

## LLM Judgment Boxing

When a step needs semantic judgment, make the agent fill only a small structured artifact:

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

Rules:

- Define allowed enum values inline.
- Give boundary examples when labels are easy to confuse.
- Use an extractor script to provide only the fields needed for judgment.
- Use a merge script to copy raw fields from source data and merge only authorized judgment fields.
- Validate counts, required fields, enum values, date formats, placeholder leakage, and raw-field preservation.

## Validation Gate Design

Prefer hard checks:

- File exists and is non-empty.
- JSON/YAML parses.
- Schema matches.
- `total == len(items)` or equivalent count consistency.
- Enum values are legal.
- Required fields are non-empty.
- No placeholders leaked.
- Raw source fields are unchanged.
- Rendered output contains required sections and no forbidden constructs.
- External action has explicit success evidence.

Use soft checks only when hard checks are impossible. Use human gates for external sending, irreversible actions, compliance-sensitive decisions, or subjective quality.

Never accept "agent should carefully check" as the only validation.

## Failure Handling Standard

Every step needs a specific policy:

- Hard fail: stop or require human review.
- Soft fail: retry with a limit.
- Partial fail: skip/degrade and record status.
- Validation fail: regenerate only the authorized output, then re-run validation.
- External action fail: do not retry blindly; require idempotency or human approval.

Always specify retry count and stop condition.

## Review Checklist

Before finalizing a chain, check:

- Is the runtime `SKILL.md` thin?
- Are business details in `plans/`, not in the engine?
- Does every step have 输入 / 任务 / 输出 / 验证命令 / 验证失败处理 / 下一步?
- Does every step do one kind of work?
- Does validation check structure and content, not just existence?
- Are raw/source fields protected from agent edits?
- Are LLM judgment fields boxed into enums and small summaries?
- Are failure policies bounded?
- Is there a `TERMINAL`?
- Are hidden dependencies named: cwd, credentials, time, login state, external tools, schedules?
- Are irreversible actions behind human or explicit external gates?
- Does the executing agent avoid reading future steps?

## Output Modes

### Mode A: Design A New ARG Chain

Use when the user asks to design, build, or convert a task into ARG.

Output:

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

### Mode B: Review An Existing Chain

Use when the user provides a skill, plan, chain, or Step Contract and asks whether it is good.

Output:

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

### Mode C: Convert Existing Skill To arg-xxx

Use when the user wants to optimize or convert an existing skill.

Output:

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

### Mode D: Turn A Vague Task Into Requirements

Use when the user only has an idea.

Output a compact requirements brief:

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

## Final Response Standard

End with the next concrete action. For design-only requests, ask whether to create the file-level deliverable. For generation requests, report changed/created files and verification evidence.

Good:

```text
我可以继续把它落成 `arg-competitor-monitor/`：薄 `SKILL.md`、4 个 step contracts、2 个验证脚本。你确认要文件级交付物的话，我下一步直接生成。
```

Good after file generation:

```text
已生成 `skills/arg-foo/`。关键文件是 `SKILL.md`、`plans/step-00-start.md`、`plans/step-01-fetch.md`、`scripts/validate_step_01.py`。已检查每个 step 都包含六个必需 section，且终点为 `TERMINAL`。
```

Bad:

```text
我们应该持续优化 agent 的可靠性。
```
