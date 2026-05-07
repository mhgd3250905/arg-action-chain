# 三分钟上手

这份指南帮你搭出第一条 ARG 行动链路。别一上来搞宏大架构，先跑通三步：获取输入、语义判断、生成结果。

## 1. 复制 starter

```bash
cp -r starter-kit my-first-arg-chain
cd my-first-arg-chain
```

如果你在 Windows PowerShell：

```powershell
Copy-Item -Recurse starter-kit my-first-arg-chain
Set-Location my-first-arg-chain
```

## 2. 改 SKILL.md

`SKILL.md` 只保留三类信息：

- 什么时候触发
- 当前步从哪里开始
- 如何循环读取 step、执行、验证、进入下一步

不要把完整业务流程全塞进 `SKILL.md`。这会直接破坏逐步揭示。是的，很多人第一步就会这么干，然后怪 Agent 不听话，挺冤但也不冤。

## 3. 写第一张 Step Contract

从 `plans/step-01-fetch.md` 开始。它只做一件事：准备输入数据。

一个合格 step 至少回答：

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

