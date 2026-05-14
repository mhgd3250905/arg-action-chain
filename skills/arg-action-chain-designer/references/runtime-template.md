# 运行时 Skill 模板

生成可运行 ARG skill 时使用本文件。不要把完整业务地图写进 runtime `SKILL.md`；业务地图存在 step 文件中，并在运行时逐步揭示。

## 标准交付结构

```text
arg-name/
├── SKILL.md
├── plans/
│   ├── step-00-start.md
│   ├── step-01-fetch.md
│   ├── step-02-process.md
│   └── step-NN-final.md
├── scripts/
│   ├── extract_for_judgment.*
│   ├── merge_or_transform.*
│   └── validate_*.*
└── output/
```

`SKILL.md` 必须薄。业务细节放进 `plans/`，确定性处理放进 `scripts/`，运行产物放进 `output/`。

## 路径放置策略

上面的目录树是逻辑结构，不强制所有文件都放在已安装 skill 目录里。

按运行环境选择：

- 本地项目内一次性交付：可以生成 `skills/arg-name/`，其中包含 `SKILL.md`、`plans/`、`scripts/`、`output/`。
- 已安装 skill / 定时任务 / 后台任务：`SKILL.md` 可以放在 runtime skills 目录，`plans/`、`scripts/`、`output/` 应放在稳定可写的数据目录或项目目录中，并在 `SKILL.md` 里使用绝对路径。
- 如果输出目录可能被周期任务清理，清理 step 必须只清理 `output/`，不能删除 `plans/` 或 `scripts/`。
- 如果路径依赖登录态、工作目录、容器路径或调度器路径，必须在 step 或 runtime `SKILL.md` 中显式写出。

## 薄 SKILL.md 模板

按用户环境替换名称和路径。

````md
---
name: arg-name
description: Only use this skill when the user explicitly invokes /arg-name or clearly asks to run this ARG chain. Executes [domain] through a static progressive clue chain with validation gates.
allowed-tools: Bash
---

# arg-name

## 触发方式

仅接受显式命令触发：`/arg-name`

不要从普通自然语言问题中猜测触发，除非用户明确要求执行这条链。

```text
设 OUTPUT_DIR = "[absolute-or-project output path]"
设 PLANS_DIR = "[absolute-or-project plans path]"
设 SCRIPTS_DIR = "[absolute-or-project scripts path]"
设 "当前步" = "step-00-start"

循环：
1. 读取 PLANS_DIR/当前步.md
2. 严格按文件中的【任务】说明执行
3. 执行文件中的【验证命令】
4. 验证通过 → 读取文件末尾【下一步】，赋值给当前步
5. 验证失败 → 按文件中的【验证失败处理】执行
6. 当前步 = "TERMINAL" → 退出循环，输出执行汇报
```

起始：读取 `PLANS_DIR/step-00-start.md`。

## 关键原则

1. **逐步揭示**：你只知道当前这一步。每步末尾的【下一步】会告诉你该读哪个文件。不要推测或预判后续步骤。
2. **验证门禁**：每步必须通过验证命令才能进入下一步。验证失败必须按失败处理执行。
3. **字段受限**：当步骤要求你填写判断字段时，只填写被授权字段，不能修改 raw/source 字段。
4. **路径稳定**：命令使用约定的 OUTPUT_DIR/PLANS_DIR/SCRIPTS_DIR，不依赖未知工作目录。
5. **不得自证**：不能用“我检查过了”代替验证命令或人工门禁。
````

## 运行时禁止行为

- 不读取未来 step。
- 不修改 `plans/` 里的 step 文件，除非用户明确处于设计/维护模式。
- 不发明字段、标签、路径或下一步。
- 不跳过验证命令。
- 不用自我声明代替验证证据。
- 不把来源说明、转换历史、设计讨论写进 runtime `SKILL.md`。
