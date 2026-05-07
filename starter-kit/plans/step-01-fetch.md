# Step 01: 准备输入

## 输入

无。此示例使用本地样例数据。

## 任务

执行：

```bash
python scripts/make_sample_input.py
```

## 输出

- `output/raw-feedback.json`

## 验证命令

```bash
python -c "
import json
d=json.load(open('output/raw-feedback.json', encoding='utf-8'))
assert d['total'] == len(d['items'])
for item in d['items']:
    assert 'index' in item
    assert item.get('content','').strip()
print('PASS: step-01')
"
```

## 验证失败处理

重试最多 1 次。仍失败则终止链路。

## 下一步

`step-02-classify`

