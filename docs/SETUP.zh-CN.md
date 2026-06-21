# 安装与启动

本仓库被设计成可以离线审阅。别人 clone 后，不需要 LLM key、EvoMap 凭据，也不需要原始私有工作目录，就可以验证公开 demo。

## 依赖矩阵

| 能力 | 需要的工具 | 是否必需 |
|---|---|---|
| 阅读 Markdown/JSON 产物 | Git、文本编辑器 | 必需 |
| 跑离线 smoke check | PowerShell 5.1+、Node.js、uv、Python 3.11+ | 推荐 |
| 校验 GEP bundle | uv、Python 3.11+ | 推荐 |
| 校验 JSON 和 reviewer role 覆盖 | Node.js | 推荐 |
| 打开 replay 页面 | 现代浏览器 | 可选 |
| 打开 Flowtrace DAG 前端 | Flowtrace CLI | 可选 |
| 实时调用 EvoMap API | EvoMap 凭据 | 可选，公开 demo 不需要 |
| 实时调用 LLM | 模型/API 凭据 | 可选，公开 demo 不需要 |

## Windows 快速开始

1. 克隆仓库：

   ```powershell
   git clone https://github.com/qrx-joe/PaperSwarm-public.git
   cd PaperSwarm-public
   ```

2. 如果缺少基础工具，可以安装：

   ```powershell
   winget install Git.Git
   winget install Python.Python.3.12
   winget install astral-sh.uv
   winget install OpenJS.NodeJS.LTS
   ```

3. 创建项目内 Python 虚拟环境：

   ```powershell
   uv venv
   uv run python --version
   ```

4. 运行离线检查：

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\demo-smoke.ps1
   ```

   预期结果：

   ```text
   PaperSwarm public demo smoke: PASS
   ```

这个检查不会调用 LLM、EvoMap 或任何外部 API，只验证本地文件、JSON、reviewer role 覆盖和 GEP bundle 结构。

## 静态 replay 页面

静态 replay 页面是自包含的：

```powershell
uv run python -m http.server 8765 --bind 127.0.0.1
```

然后打开：

```text
http://127.0.0.1:8765/replay/index.html
```

因为页面内嵌了 demo event stream，也可以直接用浏览器打开 `replay/index.html`。

## Flowtrace DAG 前端

Flowtrace DAG 前端是可选的外部工具。本仓库包含 PaperSwarm 的 `trace.json` 和启动脚本，但不内置 Flowtrace CLI 二进制或 Flowtrace Web UI 源码。

如果要使用它，需要先安装 Flowtrace，并确保下面任一方式可用：

```powershell
flowtrace --help
```

或：

```powershell
Test-Path "$env:USERPROFILE\.cargo\bin\flowtrace.exe"
```

然后启动 DAG 查看器：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\serve-flowtrace.ps1
```

打开：

```text
http://127.0.0.1:3001
```

注意：Flowtrace 的 `--scope` 参数不是指 `trace.json` 所在目录，而是指“包含 trace 项目目录的父目录”。`scripts/serve-flowtrace.ps1` 已经自动处理这个细节。

## 凭据

公开 demo 不需要任何凭据。

不要提交：

- `.env`
- `node_id`
- `node_secret`
- OAuth token 文件
- EvoMap live 原始响应
- 本地 run state、账号或余额 payload

仓库只保留 `.env.example`，用于说明环境变量名称。

## 常见问题

如果 PowerShell 查看中文乱码，先切到 UTF-8：

```powershell
chcp 65001
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

如果 `demo-smoke.ps1` 报 `node not on PATH`，安装 Node.js LTS 后重新打开终端。

如果报 `uv not on PATH`，安装 uv 后重新打开终端。

如果 `serve-flowtrace.ps1` 提示缺少 Flowtrace，离线 demo 仍然可用，只是可选的 DAG 前端不可用。
