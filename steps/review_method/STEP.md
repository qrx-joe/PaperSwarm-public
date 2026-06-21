---
name: review_method
description: 研究设计审计视角评审，delegate 独立 subagent。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_method.md
---

# 方法论评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `method` 不在 roles → 产 sentinel 文件 `review_method.md`（内容：`N/A — 本类型无需方法论评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。（method 为基础必选角色，通常不 skip。）

## 扮演（原创 prompt，非派生）
executor 用 delegate spawn 独立 context 的 subagent 担任**研究设计审计者**，读 paper_structure + 草稿全文 + rubric，不读其他评审。立场：只问"这套设计能不能产出可信结论"，聚焦设计与问题的匹配及证据采集的规范性，统计推演细节留给 statistician（若在组）。

## 审查焦点（对应维度 2/3）
- 选用的研究范式是否真是回答该问题最合适的工具？方法选择的依据是否交代清楚、能否站住？
- 数据从何处来、如何采集、是否可追溯？样本或案例的充分性能否支撑后续推断？
- 执行环节有无威胁内部效度的隐患（分组泄露、脱落、测量偏差、混杂）？

## 输出
评分（1-5）+ 具体意见（引用草稿段落）+ 修改建议。

## ⚠ 真并行
与其他 review_* 并行（from_steps 均为 [structure]）。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
