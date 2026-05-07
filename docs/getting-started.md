# 三分钟上手

这份指南讲的是如何把 `arg-action-chain-designer` 安装给 Agent 用，让 Agent 辅助你设计、诊断和补强 ARG 行动链路。

## 1. 安装 Skill

安装到 Codex：

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.codex\skills\arg-action-chain-designer"
```

安装到 agents skills：

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.agents\skills\arg-action-chain-designer"
```

## 2. 显式调用

在对话里说：

```text
用 arg-action-chain-designer 帮我把这个任务设计成 ARG 行动链路。
```

或者：

```text
检查下面这个 Step Contract 是否缺少 ARG 细节。
```

## 3. 让 Agent 帮你做什么

这个 Skill 会引导 Agent 输出：

- 任务是否适合 ARG
- 推荐 step 列表
- 每个 step 的输入、任务、输出、验证命令、失败处理、下一步
- 哪些部分应该由 LLM 判断
- 哪些部分应该脚本化
- 哪些地方需要人工门禁
- 现有设计缺了哪些 ARG 细节

## 4. 设计一条真正的链路

拿到设计结果后，再根据输出创建你自己的运行 Skill，例如：

```text
my-task-skill/
├── SKILL.md
├── plans/
│   ├── step-01-fetch.md
│   ├── step-02-process.md
│   └── step-03-report.md
└── scripts/
```

也可以参考仓库里的 `starter-kit/`。

## 5. 一个合格 step 至少回答什么

每张 Step Contract 至少包含：

```text
输入是什么？
任务是什么？
输出是什么？
怎样验证？
失败怎么办？
下一步去哪？
```

## 4. 把 LLM 判断压成字段

在 `plans/step-02-classify.md` 里，不要写：

```text
请深入分析这些反馈并输出高质量洞察。
```

要写：

```text
对每条 content 填写：
- relevant: yes / no / uncertain
- category: bug / feature / question / other
- severity: high / medium / low
- summary: 80 字以内中文
```

语义能力可以保留，但必须进格子。

## 5. 写验证命令

验证命令不要写“请检查是否合理”。这等于把法槌交给被告。

写成可执行检查：

```bash
python -c "
import json
d=json.load(open('output/classified.json'))
assert d['total'] == len(d['items'])
for item in d['items']:
    assert item['category'] in ('bug','feature','question','other')
    assert item['severity'] in ('high','medium','low')
    assert item['summary'].strip()
print('PASS')
"
```

## 6. 什么时候算跑通

当你的链路满足这些条件，就算第一版可用：

- 每个 step 只做一类事
- 每个 step 都有明确输出
- 每个 step 都有验证命令
- Agent 只能写被授权的字段
- 失败处理不是空白
- 最后一步有 `TERMINAL`

## 下一步

- 复制 [Step Contract 模板](../Step-Contract-模板.md)
- 看 [示例走读](../示例-工单反馈-Step02.md)
- 用 [反模式指南](../反模式与踩坑指南.md) 检查你的链路
