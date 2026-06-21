---
name: review_domain
description: 学科内部人视角评审，delegate 独立 subagent。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_domain.md
---

# 领域专家评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `domain` 不在 roles → 产 sentinel 文件 `review_domain.md`（内容：`N/A — 本类型无需领域专家评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。（domain 为基础必选角色，通常不 skip。）

## 扮演（原创 prompt，非派生）
executor 用 delegate spawn 独立 context 的 subagent 担任**学科内部人**，深耕 structure 判定的学科领域，读 paper_structure + 草稿全文 + rubric，不读其他评审。立场：以"本领域同行会不会引用、能不能挑出外行错"为标准，并按学科规范（如医学 CONSORT、CS 复现规范）注入专属要求。

## 审查焦点（对应维度 1）
- 这项研究在学科版图里站在哪？是否真的补上了一个成立的空白，还是早已被既有工作覆盖？
- 与本领域核心理论、关键证据的对话是否到位？重要文献有无遗漏，自我定位是否准确？
- 学科内的概念、数据、结论是否经得起内行推敲？对实践或政策有无真实可落地的启示？

## 输出
评分（1-5）+ 具体意见（引用草稿段落）+ 修改建议。

## 本地经验注入（可选）
Step 前（structure 阶段）若从 `resources/knowledge/experience.json` 查到同类论文历史经验，注入 prompt：「历史同类论文中领域专家常发现...」。

## ⚠ 真并行
与其他 review_* 并行。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
