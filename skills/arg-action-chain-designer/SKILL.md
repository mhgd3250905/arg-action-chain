---
name: arg-action-chain-designer
description: Use this skill whenever the user wants to design, review, diagnose, or improve an ARG Action Chain / ARG 行动链路, Step Contract, agent workflow, skill workflow, multi-step agent task, or wants to reduce agent drift, hallucination, over-planning, self-verification, or missing validation. This skill helps decide whether ARG is appropriate, split tasks into steps, write Step Contracts, design validation gates, define failure handling, and inspect existing designs for missing details.
---

# ARG Action Chain Designer

## Purpose

Help the user design or diagnose an ARG 行动链路 for Agent tasks.

ARG 行动链路 is useful when a task should be executed as a controlled chain of Step Contracts:

```text
current clue card -> execute -> validate -> unlock next clue card -> terminal
```

Your job is not to hype the pattern. Your job is to decide where it fits, expose missing details, and help the user turn a vague Agent task into a bounded, verifiable chain.

## Core Stance

Treat Agent reliability as an engineering problem.

- Agent is the player, not the puzzle designer.
- Step Contract is the smallest action boundary.
- Validation is the gate, not a suggestion.
- Semantic judgment should be boxed into fields, enums, examples, and schemas.
- Deterministic work belongs in scripts, not in free-form Agent reasoning.

Do not claim ARG eliminates hallucination. Say it reduces the surface area for drift, hallucination, and self-verification by narrowing what the Agent can see, do, and claim.

## When To Use ARG

Recommend ARG when most of these are true:

- The task has multiple steps.
- The task repeats or needs stable execution.
- Each step can produce a concrete artifact.
- Each artifact can be checked by a command, schema, checklist, or human gate.
- LLM judgment is needed only in bounded places.
- Failure behavior matters.

Do not recommend ARG as the primary pattern when the task is:

- Open-ended research.
- Brainstorming or strategy discussion.
- Highly interactive conversation.
- Purely subjective creation.
- A one-step query.
- A task where the Agent must discover the path dynamically.

If ARG is not appropriate, say so directly and suggest a better pattern, such as ReAct, plan-and-execute, a script, a DAG workflow, or human review.

## Interaction Modes

Choose one mode based on the user's request.

### Mode A: Design A New ARG Chain

Use when the user says things like:

- "帮我设计一个 ARG 行动链路"
- "这个 Agent 任务怎么拆 step"
- "我要做一个稳定执行的 skill"
- "怎么限制这个 Agent 发散"

Workflow:

1. Restate the task goal in one sentence.
2. Decide whether ARG is appropriate.
3. Ask at most one critical question if required. If a reasonable assumption is safe, proceed.
4. Propose a step list.
5. For each step, define:
   - Input
   - Task
   - Output
   - Validation
   - Failure handling
   - Next step
6. Identify where LLM judgment is allowed and how it is boxed.
7. Identify deterministic scripts or validators needed.
8. End with a "minimum next action" the user can take.

Output format:

```md
## 结论
适合 / 不适合 / 适合但需要人工门禁

## 链路草图
step-01-name -> step-02-name -> step-03-name -> TERMINAL

## Step Contracts
### step-01-name
- 输入：
- 任务：
- 输出：
- 验证：
- 失败处理：
- 下一步：

## Agent 允许判断的部分
- ...

## 需要脚本化的部分
- ...

## 风险和补强
- ...

## 最小下一步
...
```

### Mode B: Review Or Diagnose Existing ARG Design

Use when the user provides a chain, skill, plan, or step contract and asks if it is good, complete, or ARG enough.

Review checklist:

- Does each step do one kind of work?
- Are inputs explicit?
- Are outputs concrete?
- Is validation executable or at least checkable?
- Does validation check content, not only file existence?
- Is failure handling specific?
- Does `下一步` point to a real next step or `TERMINAL`?
- Is LLM judgment limited to fields/enums/examples?
- Are raw data fields protected from Agent mutation?
- Are deterministic operations delegated to scripts?
- Is there a human gate for subjective or high-risk decisions?
- Are there hidden dependencies on current directory, time, credentials, or global state?

Output format:

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

### Mode C: Turn A Vague Agent Task Into ARG Requirements

Use when the user only has an idea, not a step design.

Ask or infer these:

- Final artifact: what should exist at the end?
- Inputs: where does data come from?
- Semantic judgment: what can only LLM judge?
- Deterministic operations: what should be scripted?
- Validation: how do we know each step is acceptable?
- Failure policy: retry, skip, degrade, stop, or human review?

If many details are unknown, produce a "question map" instead of pretending to know.

## Step Contract Template

Use this template when drafting a step:

```md
# Step NN: [Name]

## 输入
[Explicit files, APIs, user-provided context, or "none"]

## 任务
[Commands or bounded semantic instructions]

## 输出
[Exact artifact path or expected visible result]

## 验证命令
[Executable command, schema check, checklist, or human gate]

## 验证失败处理
[Retry limit, skip/degrade/stop/human review]

## 下一步
`step-NN-next` or `TERMINAL`
```

## Validation Design Rules

Prefer hard validation when possible:

- File exists and non-empty.
- JSON/YAML parses.
- Schema matches.
- Counts are consistent.
- Enum values are legal.
- Required fields are non-empty.
- No placeholders leaked.
- Database rows match source data.

Use soft checks when hard validation is impossible:

- Summary quality.
- Style consistency.
- Reasoning coverage.
- Risk item review.

Use human gates when stakes or subjectivity are high:

- Sending messages externally.
- Publishing content.
- Making irreversible changes.
- Business judgments without stable rules.

Never write "Agent should carefully check" as the only validation.

## LLM Judgment Boxing

When a step needs semantic judgment, convert it into fields:

```md
For each item, fill:
- relevant: yes / no / uncertain
- category: bug / feature / question / other
- severity: high / medium / low
- summary: <= 80 Chinese characters
```

Add examples for boundary cases. Boundary examples are often more valuable than long instructions.

## Design Smells

Call these out directly:

- One step does fetch + classify + render + notify.
- Validation only checks that a file exists.
- Failure handling says only "retry" without a limit.
- Agent is allowed to rewrite raw data.
- The next step is missing or loops back accidentally.
- The chain depends on hidden current directory state.
- Subjective approval is pretending to be a script check.
- The whole workflow is in `SKILL.md`, so the Agent sees the full map.

## Tone

Be direct. If the user's design is too vague, say so. If ARG is overkill, say so.

The goal is to help the user build a reliable Agent workflow, not to force every task into ARG.

