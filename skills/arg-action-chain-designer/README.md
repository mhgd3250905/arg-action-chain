# ARG Action Chain Designer Skill

这是给 Agent 安装使用的 Skill，用来辅助设计、诊断和补强 ARG 行动链路。

## 安装到 Codex

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.codex\skills\arg-action-chain-designer"
```

## 安装到 agents skills

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.agents\skills\arg-action-chain-designer"
```

## 典型调用

```text
用 arg-action-chain-designer 帮我把这个 Agent 任务拆成 ARG 行动链路。
```

```text
检查这个 step contract 有没有缺少 ARG 细节。
```

```text
我想限制这个 Agent 的发散和自我验收，帮我设计验证门禁。
```

