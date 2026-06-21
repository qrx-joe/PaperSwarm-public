---
name: revise
description: 修改 Worker/Verifier 对抗循环——Worker 按修改计划改，Verifier 独立四态核验改到位没，N=2 收敛或升级人工。
reads:
  - advice/revision_plan.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - review_editor/review_editor.md
  - review_method/review_method.md
  - review_domain/review_domain.md
  - review_devil/review_devil.md
  - review_statistician/review_statistician.md
  - review_reproducibility/review_reproducibility.md
  - review_ethicist/review_ethicist.md
writes:
  - paper_revised.md
  - revise_report.md
---

# 修改 Worker/Verifier 对抗循环（H4）

> 补 advice 后「没人改 + 没人验收改到位」的缺口，与上游独立评审**对称**（评审独立找问题 / 验收独立确认改到位）。本 step 设计为 PaperSwarm 原创实现。

## 解决什么问题
advice 输出修改计划后，若作者自己改自己验，两个结构性失效：
- **Self-Preferential Bias**：改自己刚写的东西，倾向维护原文、逐条反驳评审
- **Goal Drift**：改着改着偏离评审诉求

本 step 用 Worker（改）/ Verifier（独立验）对抗循环破解。

## 团队架构（Agent 工具**串行** spawn，非并行——Worker↔Verifier 是串行依赖）
| 角色 | 关注点 | 文件所有权 | 模型 |
|------|--------|-----------|------|
| lead（executor） | 展开 revision_plan 为 checklist、驱动循环、汇总 | 读 revision_plan + 各轮产出 + 写 revise_report.md | 当前会话 |
| worker | 按 checklist 逐条改 | 读 paper_draft.md + revision_plan，写 paper_revised.md + worker-roundN.md | Sonnet |
| verifier | 独立核验「改到位没」 | 只读 paper_revised.md + revision_plan + reviewer_set.roles 对应的真评审（不读 worker 说明），写 verifier-roundN.md | **Opus** |

## 收敛规则
- **重试预算 N=2**（2 轮仍不行多为结构性分歧，升级人）
- **Verifier 四态**：已修复(通过) / 部分修复(打回) / 未修复(打回) / 引入新问题(打回)
- 全「已修复」且无「引入新问题」→ 收敛
- 第 2 轮仍不通过 → 升级人工（revise_report.md 列需裁决项 + 双方论据）

## 执行（lead 驱动）
1. 读 revision_plan.md，展开 P0/P1/P2 为可核验 checklist
2. 读 `structure/reviewer_set.json` 确定 roles，verifier 据此读对应真评审（sentinel 跳过）
3. Round 1 改：spawn worker（Sonnet）按 checklist 改 paper_draft.md → `paper_revised.md` + worker-round1.md
4. Round 1 验：spawn verifier（Opus）独立读 paper_revised.md + revision_plan + roles 对应真评审（**不读 worker 说明**），四态判定 → verifier-round1.md
5. 全通过 → 汇总；否则 Round 2（worker 带 verifier 反馈二改 → verifier 二验）
6. 第 2 轮仍不通过 → 未通过项标记「需人工裁决」
7. lead 写 `revise_report.md`（收敛通过项 / 人工裁决项 + 双方论据）

## Verifier 核验要求（写进 prompt）
对每条只回答三件事，**不得评判措辞审美**（那是作者的事）：
1. 改了没（涉及章节/段落有无对应修改）
2. 实质诉求回应了没（不只看文字变化——防 Worker 换近义词式表面应付）
3. 有无引入新问题（破坏原有论证/数据/引文）

## 与上游对称
- 评审（Stage）：N 个独立 Agent **并行**找问题（delegate 真并行，roles 按类型组队）
- 验收（本 step）：独立 Verifier **串行**确认改到位（Agent 串行 spawn）
- 评审能真独立，验收也真有独立 —— 完整闭环。

## ⚠ Executor 守卫：spawn 容错
worker/verifier subagent 失败（模型/classifier 不可用等）→ 重试 ≤2 → 仍失败 lead 兜底（同 structure 守卫契约）。

## 人工介入（H4）
`revise_report.md` 的「需人工裁决项」由作者拍板后回 lead 落实，或与原评审人沟通。
