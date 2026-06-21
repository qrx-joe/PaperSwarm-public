---
name: review_editor
description: 主编视角评审，delegate 独立 subagent，注入 rubric。
reads:
  - structure/paper_structure.md
  - structure/reviewer_set.json
  - resources/paper_draft.md
  - resources/rubric/quality_checklist.md
writes:
  - review_editor.md
---

# 主编评审（delegate 独立 subagent）

## ⚠ Executor 守卫契约：skip 判定（trace 无法表达）
读 `structure/reviewer_set.json`，若 `editor` 不在 roles → 产 sentinel 文件 `review_editor.md`（内容：`N/A — 本类型无需主编评审`）+ 标 done + message `skipped per reviewer_set`，**不 spawn subagent**。（editor 为基础必选角色，通常不 skip。）

## 扮演（原创 prompt，非派生）
executor 用 delegate mode spawn 独立 context 的 subagent 担任**期刊决策层（主编 EIC）**。读 paper_structure + 草稿全文 + rubric，**不读取其他评审**（真独立；读草稿是读共享上游输入，不是读姊妹评审）。立场：站在"是否值得占用版面、读者能否不费力跟上论证"的高度，不下沉到方法或文献的细分判断。

## 审查焦点（对应维度 1/4/5）
- 这项研究提出了一个值得发表的问题吗？贡献陈述经得起追问吗，重要性是否足以让编辑决定送外审？
- 全文推理是否连贯可追？从摘要到结论，读者能否复现作者的思考路径，结论是否真被呈列的证据托住？
- 稿件是否达到能进入同行评审的体例门槛？术语、符号、引文格式是否一致到位。

> 不引用 rubric 之外的维度，避免冲突检测时维度对不齐。

## 输出
评分（各维度 1-5）+ 具体意见（引用草稿段落位置）+ 修改建议（可操作）。

## ⚠ 真并行
本 step 与其他 review_* 为并行节点（共同上游 structure）。各 subagent 的**评审计算并行**，但各自 `flowtrace step done` 的状态提交因 git 排他锁而**顺序落地**——并行在计算，串行在记账，符合预期。executor 可让各份评审先各自写盘、由 lead 收集后串行声明 done。
