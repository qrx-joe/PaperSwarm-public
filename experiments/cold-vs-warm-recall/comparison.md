# PaperSwarm 进化对照实验：Cold vs Warm

> 一句话结论：这次严格对照没有证明“recall 让常规 RCT 缺陷发现更多”，反而证明了一个更诚实也更能打的结论：PaperSwarm 的第一性价值是多专家蜂群交叉验证；EvoMap recall 通路已打通，但在 N=1 常规 RCT 场景里对结果增量有限。

---

## 1. 实验设置

| 项 | Cold 冷启组 | Warm 进化组 |
|---|---|---|
| 论文 | `exp_cold/paper_draft.md` | `exp_warm/paper_draft.md` |
| 论文类型 | 医学 RCT | 医学 RCT |
| 题目 | 利拉鲁肽对单纯性肥胖成人体重的影响 | 同左 |
| 角色组队 | editor / method / domain / devil / ethicist / statistician | 同左 |
| 历史经验注入 | 无 | 有，见 `examples/warm_recall.sanitized.json` |
| 目标 | 基线评审能力 | 检验 recall 注入是否带来新增发现 |

本实验使用同一篇 demo_b 医学 RCT 草稿，保持角色组队一致，唯一关键变量是 Warm 组注入 EvoMap recall 得到的历史评审经验。

---

## 2. 总体结果

| 指标 | Cold 冷启组 | Warm 进化组 | 解读 |
|---|---:|---:|---|
| 缺陷总数 | 54 | 50 | Warm 没有带来更多缺陷发现 |
| 角色数 | 6 | 6 | 组队一致 |
| 核心埋点命中 | 5/5 | 5/5 | 关键风险两组都抓到 |
| CI/p 不自洽 | 命中 | 命中 | 多角色独立发现 |
| 多重比较未校正 | 命中 | 命中 | 两组一致 |
| LOCF + 脱落不对称 | 命中 | 命中 | 两组一致 |
| 子组无交互 p | 命中 | 命中 | 两组一致 |
| 注册号 / IRB / 知情同意缺失 | 命中 | 命中 | 两组一致 |

**严格结论**：Warm 组在常规医学 RCT 缺陷上没有形成有效增量。原因不是 recall 没接上，而是这些问题已经被现有角色职责覆盖：statistician 本来就会查 CI/p、多重比较、LOCF；ethicist 本来就会查注册号、IRB、知情同意和 COI。

---

## 3. 关键发现

### 3.1 蜂群交叉验证是实锤卖点

两组都发现了主终点统计数字不自洽：

```text
组间差值 5.6%
95% CI 5.1–7.7
p = 0.02
```

多个角色独立指出：如果按 CI 反推，p 值应远小于 0.001，甚至约为 10^-17 量级；如果 p=0.02 成立，则 CI 不可能是 `[5.1, 7.7]`。这不是单个 Agent 的随口质疑，而是 editor / method / domain / devil / statistician 等角色从不同角度独立抓到同一硬伤。

**这就是路演主卖点**：PaperSwarm 不只是生成审稿意见，而是让多个专家视角互相验证，抓出单一审稿人容易漏掉或不敢定性的死因。

### 3.2 EvoMap recall 通路已打通

Warm 组有真实 recall 证据：

```text
experiments/cold-vs-warm-recall/examples/warm_recall.sanitized.json
```

其中召回了历史医学 RCT 经验，包括：

- 医学 RCT 必须加入 ethicist + statistician
- LOCF + 脱落不对称需敏感性分析
- CI 与 p 值需数学自洽
- 多个次要终点需要多重比较校正

因此，本实验不是“没有接入 EvoMap”的失败，而是“接入后发现常规 RCT 缺陷已被角色职责覆盖”的负结果。

### 3.3 进化当前的真实作用域

这次结果说明：对标准医学 RCT 的常规缺陷，N=1 历史经验注入主要是冗余提醒，不会明显提高发现数量。

更合理的进化作用域是：

- 角色职责没有覆盖的非常规缺陷
- 特定领域的罕见审稿经验
- 跨论文反复出现但不在基础 rubric 内的模式
- 多次 run 后形成统计意义的经验，而不是单次 seed experience

---

## 4. 评委版解读

如果评委问“进化有没有让系统变强”，不要硬吹。

建议回答：

```text
我们做了严格对照。结果很诚实：在 demo_b 这种常规医学 RCT 缺陷上，EvoMap recall 没有带来明显新增发现，因为现有专家角色已经覆盖了这些检查项。

但这不是失败。它证明了两个事实：
第一，PaperSwarm 的蜂群评审本身足够强，冷启也能通过多角色交叉验证抓住 CI/p 不自洽、LOCF 偏倚、伦理注册缺失等硬伤。
第二，EvoMap record/recall 通路已经打通，经验能被召回并注入；只是 N=1 经验对常规缺陷的增量有限，真正的进化价值需要更多跨论文样本沉淀，尤其是非常规缺陷。
```

更短版本：

```text
这次对照没有证明“进化组更会挑常规毛病”，但证明了“蜂群交叉验证已经很强”，也证明 EvoMap recall 通路真实可用。我们没有把负结果藏起来，而是用它界定了自进化的真实边界。
```

---

## 5. 演示路径

建议按这个顺序打开：

1. `exp_cold/structure/reviewer_set.json`
2. `exp_warm/structure/reviewer_set.json`
3. `examples/warm_recall.sanitized.json`
4. `exp_cold/review_statistician.md`
5. `exp_warm/review_statistician.md`
6. `exp_cold/review_devil.md`
7. `exp_warm/review_devil.md`
8. 本文件：`evolution_comparison.md`

现场不要逐页读完 reviewer 报告，只展示三个证据点：

- 两组角色一致
- Warm 组确实有 recall
- 两组都独立抓到 CI/p 不自洽，说明蜂群可靠；Warm 未显著增量，说明边界诚实

---

## 6. 最终结论

这组实验对 PaperSwarm 的作用不是“新增功能”，而是“新增可信证据”：

- 它证明 PaperSwarm 的多角色评审链条在冷启状态下已经能发现医学 RCT 的关键硬伤。
- 它证明 EvoMap recall 能召回并注入历史经验。
- 它也证明当前 N=1 经验对常规缺陷的增量有限，不能把系统吹成已经稳定自进化。

路演主线应调整为：

```text
蜂群交叉验证是当前核心能力；
EvoMap recall 是已打通的进化通路；
自进化增益需要更多真实 run 沉淀，而不是靠一次 seed experience 硬吹。
```
