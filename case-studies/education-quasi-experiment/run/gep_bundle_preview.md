# GEP 资产包预览 — PaperSwarm run_20260616

> 本次评审 + 修改验收循环封装为 EvoMap 标准 GEP 资产包（Gene + Capsule + EvolutionEvent）。
> 完整 JSON 见 `gep_bundle.json`，`bundle_hash` 由 `gep_bundle.py seal` 回填。

## 质量门（自评）
| 项 | 值 | 门槛 | 通过 |
|----|----|----|----|
| review_score（4 评审引用完整度均值） | 0.82 | — | — |
| conflict_resolution_accuracy（裁决准确率） | 0.85 | — | — |
| **outcome.score**（综合） | **0.83** | ≥ 0.7 | ✅ |
| blast_radius.files（影响产出数） | 5 | > 0 | ✅ |
| blast_radius.lines | 120 | > 0 | ✅ |

`outcome.score = (0.82 + 0.5 × 0.85) / 1.5 = 0.83` → 通过硬门槛，生成完整三资产。

## 三类资产
- **Gene** `gene-paperswarm-review-strategy-20260617`：4-Agent 蜂群评审策略模板（category=repair，tags 含 education/quantitative-quasi-experiment）
- **Capsule** `capsule-paperswarm-run_20260616`：本次案例——判级分歧 + 前测缺失冲突，裁决大修偏重写，6 P0 修改计划，Worker/Verifier 收敛（success=true, streak=1）
- **EvolutionEvent**：devil 在归因地基维度可靠性 0.90 最高；revise 教训（算术双算 / 引文核真引率）

## 评审循环亮点（路演素材）
1. **真蜂群分歧**：editor 判大修 vs devil 判重写；method 抓聚类效应 vs devil 抓前测缺失——冲突检测捕捉到真实多视角分歧
2. **裁决有据**：采纳 devil（归因地基最致命），置信度 78-85%
3. **闭环验收**：Worker 改 → Verifier 独立验，R1 打回 d 算错 → R2 双算收敛，13 条全通过

## 真发（接口就绪时）
```
evolver publish --bundle gep_bundle.json --dry-run   # 先校验
evolver publish --bundle gep_bundle.json             # 正式发
```
**现场 API 未开放时的演示话术**：「GEP bundle 已生成并通过本地结构校验（canonical hash + 硬门槛 outcome 0.83 / blast_radius 5 文件），接口开放执行 `evolver publish` 即可进 candidate 池。」
