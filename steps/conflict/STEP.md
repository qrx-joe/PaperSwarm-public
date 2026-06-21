---
name: conflict
description: 对比 reviewer_set.roles 的评审，检测冲突并生成裁决建议；作者裁决写入 author_resolution.md。
reads:
  - structure/reviewer_set.json
  - review_editor/review_editor.md
  - review_method/review_method.md
  - review_domain/review_domain.md
  - review_devil/review_devil.md
  - review_statistician/review_statistician.md
  - review_reproducibility/review_reproducibility.md
  - review_ethicist/review_ethicist.md
writes:
  - conflict_report.md
  - author_resolution.md
---

# 冲突检测与裁决（H4）

## ⚠ Executor 守卫契约：fan-in 完整性（trace 无法表达）
运行前 executor 必须：
1. 读 `structure/reviewer_set.json` 确定 `roles`（本次实际参评角色集）
2. 确认 state.json 中 roles 列出的每个 review_* 状态**均为 done**
3. 跳过 sentinel 文件（内容为 `N/A — ...` 的，即未被选中的角色），**不参与冲突检测**

任一 roles 内角色未完成则标记 conflict 为 blocked 并提示缺失项，**禁止用部分评审跑冲突检测**（缺的那位可能是唯一反对者，部分运行会产生错误的「无冲突」结论）。

## 做什么
1. 读 reviewer_set.json 的 roles，提取各份**真评审**的核心观点（sentinel 跳过）
2. 检测冲突：评价相反 / 建议矛盾 / 优先级冲突
3. 分级：🔴 严重（影响核心结论）/ 🟡 中度（局部论证）/ 🟢 轻微（风格）
4. 每个冲突给裁决建议 + 置信度（参考 `resources/knowledge/experience.json` 的历史 agent_reliability）

## 执行方式
由 executor 按本 STEP 内联执行：读取已完成的 reviewer outputs，抽取共识/分歧，写入 `conflict_report.md` 与 `author_resolution.md`。当前仓库不依赖独立冲突检测脚本。

## 人工介入（H4）
作者对每个冲突裁决：采纳 A / B / 两者 / 都不，结果写入 `author_resolution.md`（conflict 的第二个 asset，下游 advice 消费）。
