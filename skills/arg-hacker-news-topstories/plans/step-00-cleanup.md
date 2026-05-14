# Step 00：清理上一轮输出

## 输入
无。

## 任务

清理 `output/` 目录内上一轮产物，只删除本链路生成的文件。

```bash
python scripts/cleanup_outputs.py
```

## 输出

`output/` 目录存在，且不包含上一轮 Hacker News 产物。

## 验证命令

```bash
python scripts/validate_cleanup.py && echo "PASS: step-00"
```

## 验证失败处理

重试 1 次。仍失败则终止链路，报告 `清理输出目录失败`。

## 下一步
`plans/step-01-fetch-topstories.md`
