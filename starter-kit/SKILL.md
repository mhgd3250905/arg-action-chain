# My ARG Action Chain

## Trigger

Only run this chain when explicitly triggered:

```text
/my-arg-chain
```

## Engine

Set:

```text
PLANS_DIR = "plans"
CURRENT_STEP = "step-01-fetch"
```

Loop:

1. Read `PLANS_DIR/CURRENT_STEP.md`.
2. Execute only the task described in that step.
3. Run the validation command from that step.
4. If validation passes, read `下一步` and set it as `CURRENT_STEP`.
5. If validation fails, follow `验证失败处理`.
6. If `CURRENT_STEP` is `TERMINAL`, stop and report the result.

## Rules

- Do not read future steps before the current step passes validation.
- Do not modify step files while running the chain.
- Do not invent new fields or labels.
- Do not claim success without running the validation command.
- Only write the fields explicitly assigned to the Agent.

