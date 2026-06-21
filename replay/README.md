# PaperSwarm · 蜂群评审事件回放（路演演示页）

> **分工**：本页是**离线路演演示页**——双击 `index.html` 即用、零环境依赖、内嵌编排好的事件流叙事，给评委讲"故事"；flowtrace `serve`（`scripts\serve-flowtrace.ps1` 起，:3000）是**技术查看器**——实时 DAG + 原始 runs，给开发看"真相"。两者数据源独立、互不依赖、可同时开。

**用法**：双击 `index.html`（首屏即内嵌 demo，即路演剧本）；或点导航「加载数据」拖入 `events.json` 看真实 run。

**为何离线自包含**：路演现场 `serve` 可能因二进制退化/端口起不来（见 `RUNBOOK.windows.md` §6.1 的静默退化故障），内嵌 demo 是路演的保险——只要文件在，故事就能讲。
