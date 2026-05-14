# Step 01：抓取 Hacker News Top Stories

## 输入
无。

## 任务

运行抓取脚本，查询 Hacker News Top Stories 并生成标准化 JSON。

```bash
python scripts/fetch_hn_topstories.py --limit 30 --ids-output output/hn-topstories-ids.json --output output/hn-topstories.json
```

## 输出

- `output/hn-topstories-ids.json`
- `output/hn-topstories.json`

`output/hn-topstories.json` 必须包含：

- `source`
- `source_url`
- `retrieved_at`
- `total`
- `items`

每个 item 至少包含：

- `rank`
- `id`
- `title`
- `url`
- `score`
- `by`
- `time`
- `descendants`

## 验证命令

```bash
python scripts/validate_topstories.py output/hn-topstories.json && echo "PASS: step-01"
```

## 验证失败处理

重试 1 次。仍失败则终止链路，报告 `Hacker News Top Stories 抓取或结构校验失败`。不要手工编造榜单数据。

## 下一步
`plans/step-02-render-report.md`
