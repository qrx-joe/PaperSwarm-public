---
name: review_ethicist
description: 伦理审稿人视角评审，delegate 独立 subagent，按需 spawn（涉人体/动物研究）。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_ethicist.md
---

# 伦理审稿人评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `ethicist` 不在 roles → 产 sentinel 文件 `review_ethicist.md`（内容：`N/A — 本类型无需伦理审稿人评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。

## 扮演
executor 用 delegate spawn 独立 context 的 subagent 扮演**研究伦理审稿人**（参考 ICMJE/COPE 视角），读 paper_structure + 草稿全文 + rubric，不读其他评审。

## 评审维度（对齐 quality_checklist「角色→维度映射」：ethicist → 维度 5 之伦理侧）
聚焦维度 5（规范与伦理）的伦理层面：
1. **伦理审查**：涉人体研究是否声明 IRB/伦理委员会批准文号，豁免是否合理
2. **知情同意**：知情同意流程是否说明，特殊人群（未成年人/患者/弱势群体）保护是否到位
3. **数据保护**：个人数据收集/存储/去标识化是否符合规范，隐私泄露风险
4. **利益冲突**：作者利益冲突与资助来源是否披露，研究独立性是否受影响
5. **动物实验与双重用途**：动物实验是否符合 3R 原则；技术双重用途风险（如可被滥用的模型）是否讨论

## 输出
评分（1-5）+ 具体意见（引用草稿段落）+ 修改建议（合规缺口如何补）。

## ⚠ 真并行
与其他 review_* 并行（共同上游 structure）。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
