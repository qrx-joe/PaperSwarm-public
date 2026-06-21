---
name: review_statistician
description: 统计审稿人视角评审，delegate 独立 subagent，按需 spawn（定量论文）。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_statistician.md
---

# 统计审稿人评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `statistician` 不在 roles → 产 sentinel 文件 `review_statistician.md`（内容：`N/A — 本类型无需统计审稿人评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。

## 扮演
executor 用 delegate spawn 独立 context 的 subagent 扮演**生物统计/计量统计审稿人**，读 paper_structure + 草稿全文 + rubric，不读其他评审。

## 评审维度（对齐 quality_checklist「角色→维度映射」：statistician → 维度 3 之统计侧）
聚焦维度 3（证据与可复现性）的统计层面：
1. **统计前提检验**：所用方法的前提（正态/方差齐性/独立性）是否核验，违反时是否改用稳健替代
2. **效应量与置信区间**：是否报告效应量（不止 p 值），置信区间宽度是否支撑结论
3. **样本量与功效**：样本量是否有事先功效计算，事后功效是否被误用
4. **模型选择**：模型设定是否匹配数据结构与测量层级，有无过拟合/漏关键变量
5. **多重比较与选择性报告**：多次检验是否校正，p-hacking / star-chasing 痕迹

## 输出
评分（1-5）+ 具体意见（引用草稿段落 + 具体统计量）+ 修改建议（给出正确做法）。

## ⚠ 真并行
与其他 review_* 并行（共同上游 structure）。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
