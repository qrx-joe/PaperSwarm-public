---
name: structure
description: 解析论文草稿为结构化要素，并输出可插拔评审角色组队决策 reviewer_set.json，供下游评审 subagent 共用。
reads:
  - resources/paper_draft.md
writes:
  - paper_structure.md
  - reviewer_set.json
---

# 论文结构解析（H5）

## 输入约定
被评审草稿在 `resources/paper_draft.md`（每次评审前替换为新论文全文）。格式样例见 `paper_draft.example.md`。

## 做什么
用 LLM 解析草稿，产出 `paper_structure.md` + `reviewer_set.json`：
1. 识别论文类型（journal-paper / thesis / essay）
2. 提取各章节（标题/摘要/关键词/引言/文献综述/方法/结果/讨论/结论/参考文献），标注完整性与字数
3. 推断学科领域、研究方法（定量/定性/混合）、数据来源
4. **组队决策**：依据学科/方法/类型，从角色池（editor/method/domain/devil/statistician/reproducibility/ethicist）选出本次应跑的角色集，写入 `reviewer_set.json`

## 组队规则（角色池 → 角色集）

| 论文特征 | 角色集 |
|---|---|
| 通用社科/教育 | editor, method, domain, devil |
| 医学 / RCT / 涉人体研究 | + ethicist, statistician |
| CS / 计算 / 实证（含代码/数据） | + reproducibility |
| 计量 / 定量密集 | + statistician |

> editor/method/domain/devil 为基础必选四角色，其余按上表叠加。规则可叠加（如医学定量 RCT = 基础4 + ethicist + statistician）。

## reviewer_set.json 结构

```json
{
  "paper_type": "medical-rct",
  "discipline": "临床医学",
  "method": "定量RCT",
  "roles": ["editor", "method", "domain", "devil", "ethicist", "statistician"],
  "role_rationale": {
    "ethicist": "涉人体研究需 IRB / 知情同意审查",
    "statistician": "RCT 需核验随机化、样本量计算、统计前提"
  }
}
```

## 质量门
- 至少识别 5 个核心章节
- 论文类型已识别
- 学科 + 研究方法已提取（决定下游领域专家 prompt 与组队）
- `reviewer_set.json` 合法：roles 非空、含基础四角色、role_rationale 覆盖所有非基础角色

## ⚠ Executor 守卫契约：H5 人工门（trace 无法表达）
Flowtrace 把 structure→review_* 视为纯数据依赖，**但本步后有一道 H5 人工确认门**：
**spawn 评审 subagent 前，executor 必须用 AskUserQuestion 让作者确认论文类型/学科 + structure 推荐的角色集（roles），作者可增删角色，未经确认禁止 spawn。**
未经确认就 spawn = 直接消耗整个评审 token 成本（成本命门）。`flowtrace show --downstream structure` 重跑时同样适用。

## ⚠ Executor 守卫契约：评审 spawn 容错（实跑教训）
spawn 各 review_* subagent 后，任一可能失败（模型/classifier 临时不可用、超时、限流）。处理契约：
1. **重试**：失败 subagent 重试 ≤2 次（退避 10s/30s）
2. **lead 兜底**：重试仍失败 → executor(lead) 自己补做该角色评审（读相同输入，写对应 `review_*.md`），**保证 reviewer_set.roles 全部齐备进 conflict**（fan-in 守卫要求 roles 全 done）
3. **标记降权**：lead 兜底的 review 在报告头部注明「⚠ 由 lead 补充——原 subagent 失败原因 X」，conflict 检测时对该份降权（lead 补的可能不如独立 subagent 对抗性强）

> 实跑验证（run_20260616）：domain subagent 因 classifier 临时不可用未启动，lead 兜底补成。此契约来自该教训。

## ⚠ Executor 守卫契约：skip 角色（trace 无法表达）
reviewer_set.roles 之外的角色（角色池中未被选中的）对应的 review_* 节点，executor 仍需让其产出 sentinel 文件 `review_<role>.md`（内容：`N/A — 本类型无需 <role> 评审`）并标 done + message `skipped per reviewer_set`，以满足 conflict 的 from_steps 完整性。详见各 review_*/STEP.md 的 skip 守卫。

## 经验召回与注入（评审前，本地 + EvoMap 双轨）
结构解析产出 `reviewer_set.json` 后、spawn 评审 subagent 前，executor 两步召回并合并注入各 review_* 的 prompt（「历史同类论文中，X 角色常发现...」）：
1. **本地兜底**：读 `resources/knowledge/experience.json`，按 reviewer_set 的学科/方法匹配历史 entries（agent_reliability 喂 conflict 置信度）
2. **EvoMap 进化记忆**：跑 `steps/publish/scripts/evomap_recall.py <run>/structure/reviewer_set.json`，从 EvoMap memory 召回（signals 编码学科+方法+角色，与 record 共用词表 → 同类论文 similarity 高），产出 `evomap_recall.json`（含可直接注入的 `injection_text`）

两者合并去重后注入。**降级契约**：evomap_recall 任何失败（断网/超时/空召回）→ 写空 matches、退出码 0，executor 静默回退纯本地 experience.json，评审照跑（评审鲁棒性优先于 EvoMap 演示）。
