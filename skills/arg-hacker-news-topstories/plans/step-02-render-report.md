# Step 02：渲染 Markdown 报告

## 输入

- `output/hn-topstories.json`

## 任务

运行报告渲染脚本，把标准化 JSON 转成 Markdown。

```bash
python scripts/render_report.py output/hn-topstories.json output/hn-topstories-report.md
```

## 输出

- `output/hn-topstories-report.md`

报告必须包含：

- 标题 `# Hacker News Top Stories`
- 抓取时间
- 数据来源
- 至少 1 条榜单条目

## 验证命令

```bash
python scripts/validate_report.py output/hn-topstories-report.md output/hn-topstories.json && echo "PASS: step-02"
```

## 验证失败处理

重试 1 次。仍失败则终止链路，报告 `Hacker News 报告渲染失败`。

## 下一步
`TERMINAL`
