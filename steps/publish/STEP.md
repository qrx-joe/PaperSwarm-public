---
name: publish
description: 把本次评审封装为 EvoMap 标准 GEP 资产（Gene+Capsule+EvolutionEvent），本地结构校验 + canonical hash 后生成 publish payload，真发留接口就绪一行命令。
reads:
  - archive/review_archive.md
  - archive/experience_update.json
  - advice/revision_plan.md
  - conflict/conflict_report.md
  - structure/paper_structure.md
  - resources/publish/gene_template.json
writes:
  - gep_bundle.json
  - gep_bundle_preview.md
  - publish_payload.json
---

# 资产封装与发布（H4 · C 方案：dry-run 优先 + fallback）

## 背景（C 方案）
现场 EvoMap API 不给/未知，本 step 不赌真发：本地生成规范 GEP bundle + 结构校验 + canonical hash + publish payload，真发留接口就绪一行命令。archive 已保证本地经验闭环兜底，publish 是 EvoMap 叙事的加分项。

## 做什么

### 1. 质量自评（按 PRD §6.2 公式）
- `review_score` = reviewer_set.roles 各份真评审文本引用完整度的均值（0-1；引用了段落/句子位置才算，泛泛建议不计；sentinel 跳过）
- `blast_radius.files / lines` = 从 revision_plan 实算（影响文件数 / 行数）
- `conflict_resolution_accuracy` = 冲突裁决后修改效果的预估准确率（0-1）
- `outcome.score = (review_score + 0.5 × conflict_resolution_accuracy) / 1.5`
- **硬门槛**：`outcome.score ≥ 0.7` 且 `blast_radius > 0` → 生成完整三资产；否则**仅生成 EvolutionEvent**（记录失败教训，不进 Capsule 候选池）

### 2. 生成三类资产
- **Gene**：评审策略模板（静态，从 `resources/publish/gene_template.json` 复制，填 timestamp / discipline / method / outcome_score / node_id）
- **Capsule**：本次案例（填 top_conflict 摘要、resolution 裁决、outcome；blast_radius 从 revision_plan 实算）
- **EvolutionEvent**：事件日志（填 conflict_patterns、agent_reliability 按 reviewer_set.roles 各评审评分、lesson）

### 3. 组 bundle
写 `gep_bundle.json`（结构见下），写 `gep_bundle_preview.md`（人类可读：三类资产摘要 + 质量门结果 + bundle_hash + fallback 话术）。

### 4. 确定性后处理（LLM 算 hash 会错，必须调脚本）
```
python3 steps/publish/scripts/gep_bundle.py seal gep_bundle.json
```
脚本做：canonical_json（所有层级 key 递归排序）+ sha256 回填 `bundle_hash` + 结构校验（三资产齐全 / outcome≥0.7 / blast_radius>0 / Gene.validation≥10字符）。**校验不过则修 bundle 再 seal，直到 ✅ PASS。**

### 5. publish payload
写 `publish_payload.json`（gep-a2a envelope，assets = 三资产），附 fallback 话术。

## gep_bundle.json 结构
```json
{
  "protocol": "gep-a2a",
  "bundle_id": "paperswarm-{{run_id}}",
  "created_at": "{{ISO8601}}",
  "quality_gate": { "outcome_score": 0.78, "blast_radius_files": 2, "blast_radius_lines": 120, "gate_passed": true },
  "assets": [ {Gene}, {Capsule}, {EvolutionEvent} ],
  "bundle_hash": "（由 gep_bundle.py seal 回填，勿手填）"
}
```

## 真发（接口就绪时，一行命令）
```
evolver publish --bundle gep_bundle.json --dry-run   # 先 dry-run 校验（不扣 credits）
evolver publish --bundle gep_bundle.json             # 正式发
```
现场 API 未开放时，演示话术：「GEP bundle 已生成并通过本地结构校验（canonical hash + 硬门槛），接口开放执行 `evolver publish` 即可进 candidate 池。」

## 脚本
- `steps/publish/scripts/gep_bundle.py seal <bundle>` — 校验 + canonical hash 回填 + 写回
- `steps/publish/scripts/gep_bundle.py validate <bundle>` — 只校验，不改文件

## 质量门
- [ ] gep_bundle.json 含 Gene + Capsule + EvolutionEvent 三资产
- [ ] `python3 steps/publish/scripts/gep_bundle.py validate gep_bundle.json` 输出 ✅ PASS
- [ ] bundle_hash 已回填（非占位字符串）
- [ ] outcome.score ≥ 0.7 且 blast_radius > 0（或明确标记未达门槛、仅 EvolutionEvent）
