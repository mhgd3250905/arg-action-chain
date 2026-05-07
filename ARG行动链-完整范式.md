# ARG 行动链路：一种控制 LLM Agent 发散的工程范式

## 1. 问题

LLM Agent 在多步任务里容易出现三类问题：

1. **超前规划**：看到任务全貌后，自行修改流程。
2. **行动发散**：面对模糊指令时，发明新字段、新标签或额外产物。
3. **自我验收**：自己生成结果，自己宣布结果正确。

这些问题的根源不是模型“不努力”，而是系统给了它过大的视野和自由度。

ARG 行动链路的思路是：不要把 Agent 当成全权架构师，而是把它放进一条逐步解锁的行动链中。它每次只读取当前线索卡，完成当前任务，通过验证后才能进入下一步。

## 2. 核心隐喻

ARG 游戏的玩家不会一开始拿到完整地图。玩家只能看到当前线索，解开后获得下一条线索。

映射到 Agent 工程：

| ARG 元素 | Agent 工程映射 |
| --- | --- |
| 线索卡 | `plans/step-02-process.md` |
| 解谜 | 严格执行当前 step |
| 通关条件 | 可执行验证命令 |
| 下一条线索 | 当前 step 末尾的“下一步” |
| 游戏终点 | `TERMINAL` |

这不是为了好玩，是为了限制 Agent 的上下文视野和行动边界。

## 3. Step Contract

每个 step 都是一份自包含契约，至少包含六个字段：

```md
## 输入
明确的数据来源或文件路径。

## 任务
可执行命令，或被严格限定的语义判断任务。

## 输出
当前步骤必须产出的文件、对象或结果。

## 验证命令
用脚本、断言、schema 或 exit code 验证产物。

## 验证失败处理
失败后重试、跳过、降级或终止。

## 下一步
下一个 step 文件名，或 TERMINAL。
```

Step Contract 的重点不是“写得详细”，而是让 Agent 没有理由猜。

## 4. 三个约束

### 4.1 视野约束

`SKILL.md` 或 runner 只保存循环引擎：

```text
当前步 = step-01-fetch

循环：
  读取 plans/当前步.md
  执行任务
  执行验证命令
  验证通过 -> 读取下一步
  验证失败 -> 按失败处理执行
  当前步为 TERMINAL -> 结束
```

具体业务逻辑不要写在引擎里。引擎越短，Agent 越难在全局上乱动。

### 4.2 行动约束

能用脚本做的事情，不要让 Agent 自由发挥。

```bash
python scripts/extract_for_judgment.py input/raw.json tmp/judge.json
python scripts/merge_judgments.py input/raw.json tmp/judge-out.json output/final.json
```

需要 LLM 判断时，把任务压成有限字段：

| 字段 | 允许值 | 说明 |
| --- | --- | --- |
| relevant | yes / no / uncertain | 是否与目标主题相关 |
| category | bug / feature / question / other | 反馈类型 |
| severity | high / medium / low | 影响程度 |
| summary | 80 字以内中文 | 对原文做短摘要 |

Agent 输出结构化 JSON，而不是一段“看起来很专业”的散文。

### 4.3 验收约束

验证必须可执行：

```bash
python -c "
import json
d=json.load(open('output/final.json'))
assert d['total'] == len(d['items'])
for item in d['items']:
    assert item['category'] in ('bug','feature','question','other')
    assert item['severity'] in ('high','medium','low')
    assert item['summary'].strip()
print('PASS')
"
```

Agent 的口头承诺不算验收。exit code、schema、断言和数据一致性才算。

## 5. 虚构示例：公开反馈处理链

下面是一个脱敏示例，不对应任何真实生产系统。

```text
step-01-fetch
  拉取公开反馈数据 -> output/raw.json
  验证：文件存在、JSON 合法、items 数量一致

step-02-classify
  提取待判断字段 -> Agent 填写 category/severity/summary -> 合并
  验证：枚举合法、摘要非空、原始字段未被修改

step-03-render
  生成 HTML 报告
  验证：报告存在、关键区块齐全、无占位符泄漏

step-04-notify
  发送或保存通知结果
  验证：状态文件存在，包含 sent/skipped/failed

TERMINAL
```

关键点：Agent 只能影响 `category`、`severity`、`summary` 等被授权字段。原始 `content`、`url`、`author`、`created_at` 由合并脚本从 raw 数据复制。

## 6. 失败设计

每个 step 必须定义失败策略：

- **硬失败**：凭据失效、外部服务不可用、输入不存在。通常停止或跳过当前分支。
- **软失败**：网络抖动、临时格式异常。允许有限重试。
- **降级继续**：某个数据源失败，但整体报告仍可生成。
- **人工确认**：语义质量或业务口径无法机器判断时，引入人工门禁。

别只设计成功路径。只设计成功路径的流程，现实里通常死得很有仪式感。

## 7. 边界

ARG 行动链路不是安全沙箱。如果 Agent 仍有全目录读取权限，它理论上能读到其他 step。这里的“视野约束”首先是工程协议约束；若要强隔离，需要配合权限、沙箱或独立执行环境。

它也不是万能框架。开放式研究、强交互讨论、主观创作不适合硬套。它最适合重复执行、结构化产出、可验证、多步骤的数据型任务。

## 8. 总结

ARG 行动链路的本质是：

> 把 Agent 能看到的、能做的、能写的、能声称完成的范围，压缩到一个 Step Contract 内。

Agent 是玩家，不是出题人。  
Step Contract 是最小行动边界。  
验证命令是唯一验收权威。

