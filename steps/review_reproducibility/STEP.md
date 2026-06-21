---
name: review_reproducibility
description: 复现审稿人视角评审，delegate 独立 subagent，按需 spawn（含代码/数据/实验的论文）。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_reproducibility.md
---

# 复现审稿人评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `reproducibility` 不在 roles → 产 sentinel 文件 `review_reproducibility.md`（内容：`N/A — 本类型无需复现审稿人评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。

## 扮演
executor 用 delegate spawn 独立 context 的 subagent 扮演**复现性审稿人**（参考 OpenReview/ML 复现 track 视角），读 paper_structure + 草稿全文 + rubric，不读其他评审。

## 评审维度（对齐 quality_checklist「角色→维度映射」：reproducibility → 维度 3 之复现侧）
聚焦维度 3（证据与可复现性）的可复现层面：
1. **代码与数据开放**：代码/数据/模型权重是否公开，许可证是否允许复用，访问门槛是否说明
2. **实验可复跑**：随机种子、超参数、软件版本/环境是否记录，能否从描述复现关键数字
3. **基准公平性**：对比基线是否公平（同数据/同预处理/同算力），有无对己有利的不公平设置
4. **结果稳定性**：多次运行方差是否报告，结论是否依赖单次 lucky run，消融是否充分
5. **声明与证据匹配**：方法章节描述是否足以支撑他人独立复现，缺哪些关键细节

## 输出
评分（1-5）+ 具体意见（引用草稿段落 + 指出缺失的复现要素）+ 修改建议。

## ⚠ 真并行
与其他 review_* 并行（共同上游 structure）。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
