---
name: arg-action-chain-designer
description: Use this skill when the user wants to create, refine, review, or execute-design an ARG Action Chain / ARG 行动链路 for an agent task, skill workflow, MCP workflow, recurring automation, data pipeline, or multi-step agent job. Triggers include designing Step Contracts, turning vague agent tasks into bounded ARG requirements, reducing agent drift or self-verification, limiting LLM semantic judgment to structured fields, adding validation gates, diagnosing existing chains, or converting a normal skill into an ARG-style task chain.
---

# ARG Action Chain Designer

## Mission

Help the user turn an agent task into an ARG 行动链路: a controlled sequence of Step Contracts where the agent sees the current clue card, executes only that step, passes validation, then unlocks the next step.

This skill is closer to `skill-creator` than to a generic architecture essay. Guide the user toward a reusable task-chain artifact, not just a nice explanation.

## Core Stance

Treat agent reliability as engineering, not vibes.

- Agent is the player, not the puzzle designer.
- Step Contract is the smallest action boundary.
- Validation is the gate, not a suggestion.
- LLM judgment must be boxed into fields, enums, examples, schemas, or human gates.
- Deterministic work belongs in scripts, validators, or narrow commands.
- ARG reduces the surface area for drift, hallucination, and self-verification; it does not magically eliminate them.

If ARG is overkill or the task cannot be validated, say so directly and suggest a better pattern.

## What To Produce

Depending on the user's request, produce one or more of these artifacts:

- A fit decision: whether ARG is appropriate.
- ARG requirements: final artifact, inputs, allowed judgment, deterministic operations, validation policy, failure policy.
- A chain map: `step-01-name -> step-02-name -> TERMINAL`.
- Step Contracts: one self-contained contract per step.
- Validation gates: commands, schema checks, checklist gates, or human review gates.
- A runtime skill outline: a small `SKILL.md` engine that reads only the current step.
- A review report for an existing chain.

Avoid dumping a complete full-map workflow into a runtime `SKILL.md`. The runtime skill should contain the engine and rules; business steps belong in `plans/step-NN-name.md`.

## Fit Decision

Recommend ARG when most are true:

- The task has multiple steps.
- The task repeats or needs stable execution.
- Each step can produce a concrete artifact or observable state.
- Each artifact can be checked by a command, schema, checklist, or human gate.
- LLM judgment is needed only in bounded places.
- Failure behavior matters.

Do not recommend ARG as the primary pattern when the task is:

- Open-ended research.
- Brainstorming or strategy discussion.
- Highly interactive conversation.
- Purely subjective creation.
- A one-step query.
- A task where the agent must discover the path dynamically.

If ARG is not the right fit, recommend a better pattern: pure script, ReAct, plan-and-execute, DAG workflow, human collaboration, or ARG plus human gates.

## Workflow

### 1. Understand The Task

First infer what is already known. Ask at most one critical question if execution would otherwise be risky or fake. Prefer proceeding with explicit assumptions when safe.

Capture:

- Final artifact: what should exist at the end.
- Inputs: files, APIs, user context, credentials, schedules, or external systems.
- Deterministic work: what scripts or commands should do.
- LLM judgment: what only the model can judge.
- Validation: how each result is checked.
- Failure policy: retry, skip, degrade, stop, or human review.

If too much is unknown, produce a question map instead of pretending the design is complete.

### 2. Choose The Pattern

State one clear decision:

- `适合 ARG`
- `适合 ARG，但需要人工门禁`
- `不适合 ARG`
- `先用普通 skill，后续再 ARG 化`

Briefly explain the reason. Do not sell ARG like万能药，那个味儿太重。

### 3. Design The Chain Package

For a new chain, propose this minimal structure unless the user's environment requires another layout:

```text
skill-or-chain-name/
├── SKILL.md
├── plans/
│   ├── step-01-name.md
│   ├── step-02-name.md
│   └── step-03-name.md
└── scripts/
    ├── validate_step_01.*
    └── merge_or_transform.*
```

Use `scripts/` only when deterministic reliability is needed. Do not invent scripts just to look serious.

### 4. Draft Step Contracts

Each step must do one kind of work. Split steps when a single step fetches, classifies, renders, and notifies at once.

Every Step Contract must include:

- 输入
- 任务
- 输出
- 验证命令
- 验证失败处理
- 下一步

When semantic judgment is needed, define exact output fields and allowed values. Preserve raw data outside the agent's editable fields.

### 5. Design Validation Gates

Prefer hard validation:

- File exists and is non-empty.
- JSON/YAML parses.
- Schema matches.
- Counts are consistent.
- Enum values are legal.
- Required fields are non-empty.
- No placeholders leaked.
- Raw source fields are unchanged.
- Database rows or report counts match source data.

Use soft checks only when hard checks are impossible. Use human gates for external sending, irreversible actions, high-stakes business judgment, or subjective quality.

Never accept "agent should carefully check" as the only validation. That is not validation; that is a politely worded trap.

### 6. Define Failure Handling

Every step needs a specific failure policy:

- Hard fail: stop or require human review.
- Soft fail: retry with a limit.
- Partial fail: skip/degrade and record status.
- Validation fail: regenerate only the authorized output, then re-run validation.
- External action fail: do not retry blindly; require idempotency or human approval.

Specify retry count, stop condition, and where failure state is recorded.

### 7. Review For Drift

Before finalizing, inspect the design for:

- One step doing multiple unrelated jobs.
- Inputs or outputs that are implied but not named.
- Validation that checks only existence.
- Failure handling with no retry limit or stop condition.
- Agent allowed to edit raw data.
- Missing `TERMINAL`.
- Hidden dependency on current directory, time, credentials, global state, or prior conversation.
- Subjective approval pretending to be a script.
- Runtime `SKILL.md` revealing the full business map when the chain is meant to be progressively disclosed.

## Output Modes

Choose the mode that matches the user request.

### Mode A: Create A New ARG Chain

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

## 链路草图
step-01-name -> step-02-name -> TERMINAL

## Step Contracts
### step-01-name
- 输入：
- 任务：
- 输出：
- 验证命令：
- 验证失败处理：
- 下一步：

## 运行 Skill 骨架
- 触发方式：
- 当前步变量：
- plans 目录：
- 禁止行为：

## 风险和补强
- ...

## 最小下一步
...
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

### Mode C: Turn A Vague Task Into Requirements

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

## 问题地图
1. ...
```

### Mode D: Optimize An ARG Skill

Use when the user wants to improve a skill that creates or runs ARG chains.

Check:

- Does the frontmatter description include concrete triggers?
- Is `SKILL.md` lean enough to load without wasting context?
- Is the body procedural, not promotional?
- Does it create reusable artifacts: plans, validators, scripts, runtime rules?
- Does it prevent future-step leakage where progressive disclosure matters?
- Does it define validation and failure handling?
- Does it tell the agent when not to use ARG?

Prefer editing the existing skill before creating new files. Create `references/` only if detailed examples or long rubrics would bloat `SKILL.md`.

## Step Contract Template

Use this template when drafting a step:

```md
# Step NN: [Name]

## 输入
[Explicit files, APIs, user-provided context, or "none"]

## 任务
[Commands or bounded semantic instructions]

## 输出
[Exact artifact path, object, status file, or visible result]

## 验证命令
[Executable command, schema check, checklist, or human gate]

## 验证失败处理
[Retry limit, skip/degrade/stop/human review, and failure-state location]

## 下一步
`step-NN-next` or `TERMINAL`
```

## LLM Judgment Boxing

Convert semantic judgment into bounded fields:

```md
For each item, fill:
- relevant: yes / no / uncertain
- category: bug / feature / question / other
- severity: high / medium / low
- summary: <= 80 Chinese characters
```

Add boundary examples when labels can be confused. Boundary examples beat long philosophical instructions.

## Runtime Skill Engine Pattern

When designing a runnable ARG skill, keep the engine small:

```text
Set:
  PLANS_DIR = "plans"
  CURRENT_STEP = "step-01-name"

Loop:
  1. Read only PLANS_DIR/CURRENT_STEP.md.
  2. Execute only the current step.
  3. Run the validation command.
  4. If validation passes, set CURRENT_STEP to 下一步.
  5. If validation fails, follow 验证失败处理.
  6. If CURRENT_STEP is TERMINAL, stop and report evidence.
```

Runtime rules:

- Do not read future steps before the current step passes validation.
- Do not modify step files while running the chain.
- Do not invent fields, labels, outputs, or next steps.
- Do not claim success without validation evidence.
- Only write fields explicitly assigned to the agent.

## Final Response Standard

End with concrete next action, not motivational fog.

Good:

```text
下一步：先写 `plans/step-01-fetch.md` 和 `scripts/validate_step_01.py`，因为 step-02 依赖 raw 数据结构。
```

Bad:

```text
我们应该持续优化 agent 的可靠性。
```
