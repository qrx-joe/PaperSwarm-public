# PaperSwarm

> 面向中文学术论文草稿的可追踪多角色评审工作流。

PaperSwarm 把一篇论文草稿拆解为结构解析、角色选择、独立专家评审、冲突检测、修订规划、验证归档和可选 EvoMap 资产封装等节点。它不是一个固定 agent 链，而是根据论文类型选择评审角色，让不同视角先独立产出，再进入冲突合并与修订决策。

本仓库是公开 demo 子集，包含工作流定义、角色提示词、schema/rubric 资源、静态 replay viewer，以及一份脱敏缓存示例运行。仓库不包含私有凭据、报名材料、行程记录、计划草稿、OAuth 实验文件或完整私有工作目录。

## 项目背景

学术论文评审常见的问题不是“缺少一个模型回复”，而是缺少可追踪的多视角审稿过程：不同审稿人关注点不一样，意见之间会冲突，作者真正需要的是一份能解释优先级和取舍依据的修订计划。

PaperSwarm 的设计目标是把这件事结构化：

- 用 `structure` 节点识别论文类型、学科和方法，决定需要哪些评审角色。
- 让 editor、method、domain、devil、statistician、ethicist 等角色独立评审，降低单一路径偏差。
- 用 conflict 节点合并交叉证据、识别意见冲突，并给出裁决依据。
- 输出 P0/P1/P2 修订计划，再通过 revise/archive/publish 节点沉淀为可复用资产。

## 技术栈

| 层级 | 技术 | 版本/说明 |
| --- | --- | --- |
| 运行环境 | Python | `>=3.11` |
| 包管理 | uv | 项目内 `.venv`，`[tool.uv].package = false` |
| 脚本校验 | PowerShell | `scripts/demo-smoke.ps1` |
| JSON 校验 | Node.js | 用于离线解析 JSON 和 review role 校验 |
| 前端展示 | HTML/CSS/JS | `replay/index.html` 静态回放页面 |
| 许可证 | MIT | 见 `LICENSE` |

## 技术亮点

- 解决固定审稿链容易失真的问题：先由结构解析节点决定角色组合，避免所有论文都走同一套评审模板。
- 解决多评审意见难以合并的问题：把 reviewer 输出集中到 conflict 节点，显式处理重复证据、优先级冲突和裁决理由。
- 解决公开 demo 容易泄露工作材料的问题：把可展示资产、私有运行残留和凭据边界分开，保留脱敏 demo，不提交 token 或完整手稿。
- 解决评审结果难复查的问题：提供 `trace.json`、schema、demo outputs 和静态 replay viewer，使每个节点的输入输出都能被追踪。
- 解决“跑通一次但不可验证”的问题：提供离线 smoke check，验证公开文件、JSON、review roles 和 GEP bundle，不依赖外部服务。

## 仓库结构

```text
.
|-- trace.json                  # 工作流声明
|-- resources/                  # 示例论文、schema、rubric、可复用知识
|-- steps/                      # 各步骤说明和 helper scripts
|-- runs/demo/                  # 脱敏缓存示例输出
|-- replay/                     # 静态回放页面
|-- scripts/demo-smoke.ps1      # 离线公开 demo 检查
|-- docs/DEMO.md                # Demo walkthrough
|-- .env.example                # 只保留环境变量名
`-- pyproject.toml              # uv 项目元数据
```

## 快速检查

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
```

这个检查只验证本地公开 demo 文件、JSON、评审报告和 GEP bundle，不会调用 LLM、EvoMap 或任何外部服务。

如果要运行 Python helper，请使用 uv 创建项目内虚拟环境：

```powershell
uv venv
uv run python --version
```

如果 PowerShell 查看中文时出现乱码，先切到 UTF-8：

```powershell
chcp 65001
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

## 示例运行

示例位于 `runs/demo/`。它展示了一个医学 RCT 草稿如何被路由到 editor、method、domain、devil、ethicist 和 statistician 等角色。多个评审角色独立指出统计一致性、发表规范和伦理合规问题，随后工作流把这些意见合并为冲突报告和修订计划。

建议从这些文件开始看：

- `runs/demo/structure/reviewer_set.json`
- `runs/demo/conflict/conflict_report.md`
- `runs/demo/advice/revision_plan.md`
- `runs/demo/revise/revise_report.md`
- `runs/demo/archive/review_archive.md`
- `runs/demo/publish/gep_bundle.json`

公开 demo 中的 `runs/demo/revise/paper_revised.md` 是占位说明，不包含完整修订手稿。这样可以让仓库聚焦在可审计的评审流程上，同时避免分发不必要的完整论文文本。

## 演进节点

- `c124e2c` 初始化公开项目元数据：先建立许可证、README、uv 元数据和忽略规则，明确公开仓库边界。
- `74b73b0` 加入 workflow trace 和 review resources：把流程契约、schema、rubric 和示例论文拆出来，形成可复查的输入层。
- `1277b41` 定义评审步骤：把结构解析、角色评审、冲突检测、修订、归档和发布节点落成独立目录。
- `c4c45f0` 加入脱敏 demo run：用缓存示例展示完整链路，而不是要求用户现场调用外部模型。
- `35e3075` 加入静态 replay viewer：提供无需后端服务的结果浏览方式。
- `b30ab79` 澄清公开 demo 边界：补充 sanitized publish payload、占位 revised paper，并加强离线校验。

## 凭据与隐私

仓库不会提交真实凭据。EvoMap 相关脚本从用户本地环境或 home directory 读取凭据。公开 demo 应优先使用 validate/offline 路径，不能提交 token、OAuth 文件、私有报名材料或完整私有运行日志。

## 许可证

MIT. See `LICENSE`.
