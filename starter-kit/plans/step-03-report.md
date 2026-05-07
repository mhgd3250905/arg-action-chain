# Step 03: 生成报告

## 输入

- `output/classified-feedback.json`

## 任务

执行：

```bash
python scripts/render_report.py output/classified-feedback.json output/report.md
```

## 输出

- `output/report.md`

## 验证命令

```bash
python -c "
from pathlib import Path
p=Path('output/report.md')
s=p.read_text(encoding='utf-8')
assert '# Feedback Report' in s
assert 'Total:' in s
assert 'Category Breakdown' in s
print('PASS: step-03')
"
```

## 验证失败处理

重试最多 1 次。仍失败则终止链路并报告 `report_failed`。

## 下一步

`TERMINAL`

