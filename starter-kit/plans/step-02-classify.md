# Step 02: 有限字段分类

## 输入

- `output/raw-feedback.json`

## 任务

第 1 步，提取待判断数据：

```bash
python scripts/extract_for_judgment.py output/raw-feedback.json tmp/judge.json
```

第 2 步，逐条读取 `tmp/judge.json`，只填写以下字段：

| 字段 | 允许值 | 说明 |
| --- | --- | --- |
| relevant | yes / no / uncertain | 是否是有效产品反馈 |
| category | bug / feature / question / other | 反馈类型 |
| severity | high / medium / low | 影响程度 |
| summary | 80 字以内中文 | 简洁概括 |

第 3 步，将判断写入：

- `tmp/judge-out.json`

输出格式：

```json
[
  {
    "index": 0,
    "relevant": "yes",
    "category": "bug",
    "severity": "high",
    "summary": "导出按钮无响应并返回错误"
  }
]
```

第 4 步，合并：

```bash
python scripts/merge_judgments.py output/raw-feedback.json tmp/judge-out.json output/classified-feedback.json
```

## 输出

- `output/classified-feedback.json`

## 验证命令

```bash
python -c "
import json
d=json.load(open('output/classified-feedback.json', encoding='utf-8'))
assert d['total'] == len(d['items'])
for item in d['items']:
    assert item['relevant'] in ('yes','uncertain')
    assert item['category'] in ('bug','feature','question','other')
    assert item['severity'] in ('high','medium','low')
    assert item['summary'].strip()
    assert item.get('content','').strip(), 'raw content must be preserved'
print('PASS: step-02')
"
```

## 验证失败处理

重试分类最多 1 次。仍失败则保留 `output/raw-feedback.json`，标记分类失败，并进入 `step-03-report` 生成失败报告。

## 下一步

`step-03-report`

