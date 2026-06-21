# 冲突检测与裁决报告 — TempoMix 时序预测

> 评审对象：TempoMix 多尺度时序注意力模型（6 基准对比）
> 参评角色（reviewer_set.roles）：editor / method / domain / devil / reproducibility（5 份真评审）
> 跳过：statistician、ethicist（sentinel，ML 论文无 RCT 统计/伦理需求）
> 日期：2026-06-18

## 一、总体结论与判级分布

| 角色 | 判级 | 关键依据 |
|---|---|---|
| editor | **重写** | 维度5规范侧1/5跌破下限（参考文献缺失），12.4%数据不全 |
| method | **重写/大修** | 基线cherry-pick、消融仅2项、10epoch无收敛论证、不可复现 |
| domain | **重写**（2.2/5） | 2023竞品TimesNet等集体缺席、多尺度被Autoformer/PatchTST覆盖 |
| devil | **拒稿重投**（3/10） | 基线拼接+选择性报告+单次运行+12.4%算不出 |
| reproducibility | **重写**（1.4/5） | 代码录用前不公开+基线拼接+单次无方差（三条阻断性缺陷） |

**判级共识**：与医学 run 的"大修 vs 重写"分歧不同，CS run 五角色**一致判重写/拒稿**——基线拼接是致命伤，所有角色独立认可。分歧仅在严厉度（devil/reproducibility 最严，editor 相对温和）。

## 二、共识问题（≥2 位独立评审提及）

### P0（严重）

| # | 共识问题 | 共识角色 | 强度 |
|---|---|---|---|
| C1 | **基线跨论文拼接（"各基线原文最佳结果"），非统一环境复现，对比无效** | method / devil / reproducibility | ★★★★★ |
| C2 | **选择性报告：192/336 步"优势扩大"却只报 96 步** | devil / reproducibility | ★★★★★（devil 升格为学术诚信红线） |
| C3 | **单次运行无方差，0.0x 量级优势落在 seed 噪声里** | devil / reproducibility | ★★★★★ |
| C4 | **代码"录用后公开"，录用前零可获得性** | editor / devil / reproducibility | ★★★★ |
| C5 | **参考文献完全缺失，正文模型名无引文** | editor / domain / devil | ★★★★ |
| C6 | **"平均降低12.4%"无法从正文数据复算**（正文仅2数据集具体值，余"均最优"无数字） | editor / devil | ★★★★ |

### P1（中度）

| # | 共识问题 | 共识角色 |
|---|---|---|
| C7 | 消融仅2变体+1数据集，撑不起"多尺度交互是关键"的因果论断 | method / devil / reproducibility |
| C8 | 相关工作过薄，2023 直接竞品（TimesNet/Pyraformer/Crossformer）缺席 | domain / editor / devil |
| C9 | 10 epoch 训练未证收敛，却全面超越收敛基线，评测口径存疑 | method / devil / reproducibility |
| C10 | 方法描述不可复现（尺度偏置/融合公式/超参表/硬件/参数量对比缺失） | devil / method |

## 三、分歧与互补

### 分歧（严厉度，非方向）：选择性报告的定性
- **devil**：升格为"学术诚信红线"——"作者藏起对自身最有利的长程证据，审稿人对全文失去信任"。
- **reproducibility**：定性为"典型选择性报告/cherry-picking"，措辞稍温和，但同样要求补完整 horizon 表。
- **裁决**：采纳 devil 的严厉定性作为风险提示，行动项一致（补完整 96/192/336 表）。

### 角色独占发现（互补，证明可插拔价值）
- **reproducibility 独占**：系统的 5 子项复现评分（代码1/基线1/可复跑2/稳定性1/选择性2）+ 具体缺失要素清单（匿名仓库/checkpoint/requirements/硬件/seed）。**本次 CS run 的 MVP 角色**——医学 run 里它是 sentinel，CS run 里它贡献了最系统的缺陷框架。
- **domain 独占**：TimesNet/Pyraformer/Crossformer 等 2023 竞品集体缺席 + "多尺度分解"被 Autoformer/PatchTST 机制覆盖（贡献增量存疑）+ 引言"现有方法单一尺度"是 strawman。
- **devil 独占**：12.4% 的复算崩盘（2 数据集已知值平均 11.75%，凑不出 12.4%）+ 消融差距 0.045 打在噪声区间。

## 四、修改路线图

| 优先级 | 修改项 | 来源 |
|---|---|---|
| P0 | 统一环境复现 5 基线，报告复现值+原文值+偏差 | C1 |
| P0 | 每数据集 ≥5 seed，报告 mean±std + 显著性检验（Diebold-Mariano） | C3 |
| P0 | 补完整主结果表（6数据集 × 96/192/336 × MSE/MAE × mean±std），能复算12.4% | C2,C6 |
| P0 | 提交时附匿名代码仓库 + 完整参考文献 | C4,C5 |
| P1 | 消融扩到 ≥3 数据集 + 分解粒度/融合方式敏感性 + w_k 权重分析 | C7 |
| P1 | 重写相关工作，诚实定位（Autoformer/DLinear 分解范式延伸，非"别人不做多尺度"） | C8 |
| P1 | 补方法细节（尺度偏置/融合公式/超参表/硬件/参数量对比） | C10 |

## 五、蜂群价值实证 + 跨学科对比（差异化卖点）

| 维度 | 医学 RCT run | CS ML run |
|---|---|---|
| 组队 | 基础4 + ethicist + statistician | 基础4 + reproducibility |
| skip | reproducibility（无代码） | statistician + ethicist（无RCT/伦理） |
| 判级分歧 | 大修 vs 重写（明显分歧） | 一致重写/拒稿（共识强） |
| MVP 角色 | statistician（修正devil偏倚断言） | reproducibility（系统复现缺陷框架） |
| 交叉验证 | CI/p不自洽（devil+statistician） | 基线拼接（devil+reproducibility） |

**两次 run 证明**：structure 按 type 组队正确（医学无 reproducibility、CS 无 ethicist/statistician），可插拔池按学科激活对应专家角色，每个被选入的角色都贡献了独占发现。这是"7角色可插拔池"差异化的实锤。
