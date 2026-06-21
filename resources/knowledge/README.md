# 本地知识库（resources/knowledge/）

> 写作经验与评审经验沉淀在本地，跨论文复用，无外部平台依赖。

## 文件
- `knowledge_introduction_moves.json` — 引言评审与写作要点（四个说服任务，原创设计）
- `knowledge_quality_dimensions.json` — 5 维度质量评审经验（评审角色池 rubric 的结构化来源；markdown 注入版见 `rubric/quality_checklist.md`）
- `experience.json` — 跨论文累积的评审经验（archive step 每次追加，structure/review 查询注入）

## 用途
1. **评审 rubric**：review_* 读 `../rubric/quality_checklist.md` + 对应 knowledge，作为评分维度
2. **经验闭环**：archive 提取本次经验 → `experience.json` 累积 → 下次 structure/review 查询匹配注入

## 本地经验闭环
```
评审 → archive 提取经验 → experience.json 累积 → 下次评审查询注入（按学科/方法匹配）
```
纯本地，无网络依赖。
