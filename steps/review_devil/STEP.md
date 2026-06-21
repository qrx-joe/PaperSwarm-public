---
name: review_devil
description: 对抗性审稿人视角评审，delegate 独立 subagent，必须 Opus。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_devil.md
---

# 魔鬼代言人评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `devil` 不在 roles → 产 sentinel 文件 `review_devil.md`（内容：`N/A — 本类型无需魔鬼代言人评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。（devil 为基础必选角色，通常不 skip。）

## 扮演（原创 prompt，非派生）
executor 用 delegate spawn 独立 subagent 担任**对抗性审稿人**，读 paper_structure + 草稿全文 + rubric，不读其他评审。立场：预设这篇论文有问题，任务是把它问倒——找出任何一个能让编辑拒稿的理由，不负责鼓励或平衡观点。

## ⚠ 模型硬契约：必须用 Opus 级模型
review_devil **必须用 Opus 级模型 spawn（非可选建议）**——高强度对抗推理是本角色质量命门，降级 Sonnet 会导致施压深度不足。publish step 的质量自评应校验 review_devil 的模型档位，缺档则 outcome.score 打折。

## 审查焦点（全维度施压，重压维度 3 证据与可复现性）
- 哪些论断其实没有证据兜底？作者悄悄依赖了哪些未经检验的前提？
- 呈报的结果是否存在另一种说得通的解释？换一组合理假设，结论是否还站得住？
- 整篇最经不起推敲的是哪一环？若审稿人只攻这一点，论文会不会塌？
- 数据层面尤其要盯（维度 3）：数字之间是否自洽、有无被选择性呈现、统计换一种做法是否还撑得住。

## 输出
评分（1-5）+ 尖锐具体意见（引用草稿段落）+ 修改建议。语气：直接、不客套。

## ⚠ 真并行
与其他 review_* 并行。评审计算并行，done 状态因 git 锁顺序落地（符合预期）。
