# arg-hacker-news-topstories

查询 Hacker News Top Stories，生成标准化 JSON 和 Markdown 报告。

数据源使用 Hacker News 官方公开 API：

- `https://hacker-news.firebaseio.com/v0/topstories.json`
- `https://hacker-news.firebaseio.com/v0/item/<id>.json`

## 使用

```text
/arg-hacker-news-topstories
```

## 产物

- `output/hn-topstories-ids.json`
- `output/hn-topstories.json`
- `output/hn-topstories-report.md`

## 链路

```text
step-00-cleanup -> step-01-fetch-topstories -> step-02-render-report -> TERMINAL
```
