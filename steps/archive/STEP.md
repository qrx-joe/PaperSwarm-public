---
name: archive
description: 归档本次评审结果，提取经验沉淀到本地经验库，供下次评审复用。
reads:
  - revise/revise_report.md
  - revise/paper_revised.md
  - advice/revision_plan.md
  - conflict/conflict_report.md
  - structure/reviewer_set.json
  - review_editor/review_editor.md
  - review_method/review_method.md
  - review_domain/review_domain.md
  - review_devil/review_devil.md
  - review_statistician/review_statistician.md
  - review_reproducibility/review_reproducibility.md
  - review_ethicist/review_ethicist.md
  - resources/knowledge/experience.json
writes:
  - review_archive.md
  - experience_update.json
---

# 评审归档与经验沉淀（H1）

## 做什么
1. **归档**：把本次评审完整结果（结构解析 + reviewer_set.roles 各份真评审 + 冲突 + 修改计划）汇总到 `review_archive.md`（人类可读的评审档案；sentinel 评审跳过）
2. **经验提取**：从本次评审提取可复用经验：
   - 高频问题模式（如「样本量 vs 聚类效应」「文献综述缺失」）
   - 各评审角色可靠性趋势（按 reviewer_set.roles 动态分桶，看各角色在本类论文的命中）
   - 冲突模式（哪些维度常冲突、谁更准）
3. **本地经验库合并**：跑 `build_archive.py experience_update.json`，把本次经验增量合并进 `resources/knowledge/experience.json`（去重 by run_id，跨 run 累积）——打通本地闭环，供下次评审按学科/方法召回注入
4. **EvoMap 进化记忆回写**：跑 `evomap_record.py experience_update.json`，把经验 record 到 EvoMap memory（signals 编码学科+方法+角色），让进化经过 EvoMap 网络可见

## 经验闭环（本地 + EvoMap 双轨）
```
本次评审 → experience_update.json → ┬─ build_archive.py → experience.json（本地累积，离线兜底）
                                     └─ evomap_record.py → EvoMap memory（网络沉淀，跨会话可见）
下次评审 structure → experience.json（本地）+ evomap_recall.py（EvoMap）→ 合并注入 review prompt
```
本地 experience.json 永远是 source of truth（离线兜底）；EvoMap memory 是它的网络镜像（跨会话/跨机可见，满足评分维度①「进化肉眼可见」）。

## ⚠ 降级契约（网络失败不阻断评审）
`evomap_record.py` 任何失败（断网/API 不给/超时/quota）→ 仅 print WARNING、退出码 0，经验仍完整沉淀到本地 experience.json。**评审鲁棒性优先于 EvoMap 演示**。

## 脚本
- `steps/archive/scripts/build_archive.py <experience_update.json> [--exp <experience.json>]`：纯本地合并（零网络），去重 by run_id，默认 experience.json 按脚本位置定位。
- `steps/publish/scripts/evomap_record.py <experience_update.json>`：EvoMap memory 回写（扁平 body，Bearer 鉴权，UA 绕 Cloudflare）；signals 由 `evomap_signals.py` 归一化（与 recall 共用词表）。

## 质量门
- review_archive.md 含完整评审链
- experience_update.json 结构化（可合并到 experience.json）
