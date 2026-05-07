# 示例走读：工单反馈 Step-02 分类

这是一个虚构示例，用于说明如何把 LLM 语义判断限制在 Step Contract 中。它不对应任何真实生产资料。

## Step 02：反馈分类

### 输入

- `output/raw-feedback.json`

数据结构示例：

```json
{
  "total": 2,
  "items": [
    {
      "index": 0,
      "created_at": "2026-05-07T08:30:00Z",
      "author": "user_001",
      "content": "导出按钮点击后没有反应，控制台出现 500 错误。",
      "url": "https://example.invalid/ticket/1"
    }
  ]
}
```

### 任务

第 1 步，提取待判断字段：

```bash
python scripts/extract_for_judgment.py output/raw-feedback.json tmp/judge.json
```

第 2 步，逐条判断：

| 字段 | 允许值 | 说明 |
| --- | --- | --- |
| relevant | yes / no / uncertain | 是否是有效产品反馈 |
| category | bug / feature / question / other | 反馈类型 |
| severity | high / medium / low | 对用户影响程度 |
| summary | 80 字以内中文 | 简洁概括问题 |

第 3 步，写出判断结果：

```json
[
  {
    "index": 0,
    "relevant": "yes",
    "category": "bug",
    "severity": "high",
    "summary": "导出按钮无响应并返回 500 错误"
  }
]
```

第 4 步，合并：

```bash
python scripts/merge_judgments.py output/raw-feedback.json tmp/judge-out.json output/classified-feedback.json
```

### 输出

- `output/classified-feedback.json`

### 验证命令

```bash
python -c "
import json
d=json.load(open('output/classified-feedback.json'))
assert d['total'] == len(d['items'])
for item in d['items']:
    assert item['relevant'] in ('yes','uncertain')
    assert item['category'] in ('bug','feature','question','other')
    assert item['severity'] in ('high','medium','low')
    assert item['summary'].strip()
    assert item.get('content'), 'raw content must be preserved'
print('PASS: step-02')
"
```

### 验证失败处理

重试分类最多 1 次。仍失败则保留原始数据，标记 `classification_failed`，进入人工复核队列。

### 下一步

`step-03-render`

## 设计意图

- Agent 只填写四个字段。
- 原始内容、作者、URL、时间不允许由 Agent 改写。
- validator 检查枚举、摘要、数量一致性和原始字段保留。
- 语义判断失败后不阻断原始数据保存，而是进入人工复核。

