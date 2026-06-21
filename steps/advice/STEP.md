---
name: advice
description: 汇总评审+裁决，按裁决修正冲突项后去重排序，生成 P0/P1/P2 修改计划。
reads:
  - conflict/conflict_report.md
  - conflict/author_resolution.md
writes:
  - revision_plan.md
---

# 修改建议生成（H1）

## 做什么
1. 读 `conflict_report.md` 的冲突项 + `author_resolution.md` 的作者裁决
2. **先按裁决修正冲突项**（采纳 A / B / 两者 / 都不 的裁决应用到对应建议）
3. 提取所有评审建议（问题-位置-建议），去重（同一问题多建议合并）
4. 排序：P0 必改 / P1 应改 / P2 建议改
5. 标注修改位置（章节/段落）

## 执行方式
由 executor 按本 STEP 内联执行：读取 `conflict_report.md` 与 `author_resolution.md`，应用裁决、去重排序，并写入 `revision_plan.md`。当前仓库不依赖独立修改计划脚本。

## 质量门
无重复、每条有优先级 + 位置。
