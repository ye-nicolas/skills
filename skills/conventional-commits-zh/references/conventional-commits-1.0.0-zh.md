# 约定式提交 1.0.0（中文摘录）

> 用于参考与对齐规范术语；实际提交信息仍以仓库 `.githooks/commit-msg` 规则为准。

## 概述
约定式提交规范是一种基于提交信息的轻量级约定。它提供了一组简单规则来创建清晰的提交历史；更有利于编写自动化工具。通过在提交信息中描述功能、修复和破坏性变更，使这种惯例与 SemVer 相互对应。

提交说明结构：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 关键点

- `fix`: 修复 bug（SemVer PATCH）
- `feat`: 新增功能（SemVer MINOR）
- `BREAKING CHANGE:` 脚注或 `!`：破坏性变更（SemVer MAJOR）
- 其它类型：`build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test` 等可用
- `scope`：可选，括号包围，描述影响范围，例如 `fix(parser): ...`

## 破坏性变更

- 方式 1：在类型/范围后用 `!` 标记：`feat(api)!: ...`
- 方式 2：在脚注中使用：

```
BREAKING CHANGE: <description>
```

## 示例

- 仅描述：`docs: correct spelling of CHANGELOG`
- 带范围：`feat(lang): add polish language`
- 带正文/脚注：

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request.

Reviewed-by: Z
Refs: #123
```
