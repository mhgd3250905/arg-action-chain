# Step Contract 模板

复制此模板，为每个步骤创建 `plans/step-NN-name.md`。

---

# Step NN：[步骤名称]

## 输入
<!-- 明确文件路径或数据来源 -->
- `path/to/input-file.json`
- 或：无（从外部 API 获取）

## 任务

<!-- 第 1 步：可执行的 bash 命令 -->
```bash
command-here
```

<!-- 第 2 步：如需语义判断，给出格子化选项 -->
逐条判断规则：

- **字段1**：`选项A`（判例说明）| `选项B`（判例说明）| `选项C`（判例说明）
- **字段2**：中文 ≤N 字。特定情况以 `【标记】` 开头。
- **字段3**：`选项X`（判例：xxx/yyy）| `选项Y`（判例：aaa/bbb）| `选项Z`
- **字段4**：格式要求 + 转换规则

⚠️ 相关规则说明（如 certain=no 跳过等）

<!-- 第 3 步：写入 -->
输出到 `path/to/output.json`，格式：
```json
[{"index": 0, "field1": "optionA", "field2": "...", ...}]
```

<!-- 第 4 步：合并/入库 -->
```bash
python3 scripts/merge.py input.json judgments.json > output.json
python3 scripts/ingest.py output.json
```

## 输出
- `path/to/output-file.json`
- 或：无文件输出（stdout 含特定字符串即为成功）

## 验证命令
```bash
#!/bin/bash
# 检查 1：文件存在且有内容
[ -s "output.json" ] || { echo "FAIL: missing"; exit 1; }

# 检查 2：JSON 结构有效性
python3 -c "
import json; d=json.load(open('output.json'))
assert d['total'] == len(d['items']), 'total mismatch'
for item in d['items']:
    assert item.get('summary','').strip(), 'empty summary'
    assert item['relevant'] in ('yes','uncertain'), 'invalid relevant'
    assert item['category'] in ('bug','feature','question','other'), 'invalid category'
print('ok')
" && echo "PASS: step-NN" || echo "FAIL: step-NN"
```

## 验证失败处理
<!-- 选择一种或组合 -->

**选项 A — 硬失败（不重试）**：
若 PREFLIGHT_FAILED / 登录态丢失 / 外部服务不可达 → 标记失败，不重试，继续下一步。

**选项 B — 软失败（限次重试）**：
重试最多 N 次。仍失败 → 标记失败，继续下一步。

**选项 C — 阻断失败（终止链）**：
重试最多 N 次。仍失败 → 终止流水线。

## 下一步
`step-NN-next`  ← 验证通过后读取的文件名
<!-- 或 `TERMINAL` — 流水线结束 -->
