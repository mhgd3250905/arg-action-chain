# ARG Action Chain Designer

一个用于设计 ARG 行动链路的 Agent Skill。

这个仓库现在只维护一个核心资产：

```text
skills/arg-action-chain-designer/
```

它用于帮助 Agent 把模糊的多步任务拆成 ARG 行动链路：每一步是一个 Step Contract，Agent 只执行当前步骤，通过验证门禁后再进入下一步。

## 适合做什么

- 判断一个 Agent 任务是否适合 ARG 行动链路
- 设计 step 列表和 Step Contract
- 把 LLM 判断限制到结构化字段、枚举和 schema
- 设计验证命令、人工门禁和失败处理
- 诊断已有链路是否存在发散、自检、字段幻觉等问题

## 安装

安装到 Codex：

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.codex\skills\arg-action-chain-designer"
```

安装到 agents skills：

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.agents\skills\arg-action-chain-designer"
```

## 使用

```text
用 arg-action-chain-designer 帮我把这个 Agent 任务拆成 ARG 行动链路。
```

```text
检查这个 Step Contract 有没有缺少 ARG 细节。
```

## 目录

```text
.
├── README.md
├── LICENSE
└── skills/
    └── arg-action-chain-designer/
        ├── README.md
        └── SKILL.md
```

## 核心原则

- Agent 是玩家，不是出题人。
- Step Contract 是最小行动边界。
- 验证命令是唯一验收权威。
- 语义能力只在有限字段中发挥。

## License

[MIT](./LICENSE)
