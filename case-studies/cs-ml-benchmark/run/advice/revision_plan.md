# 修改计划 — TempoMix（CS run）

> 输入：conflict_report（C1–C10）+ author_resolution

## P0（必做，否则不可投稿）
1. 统一环境复现 5 基线（同 split/seed/硬件/epoch），报告复现值+原文值+偏差 — C1
2. 每数据集 ≥5 seed，报告 mean±std + Diebold-Mariano 显著性检验 — C3
3. 补完整主结果表（6数据集 × 96/192/336 × MSE/MAE × mean±std），确保能复算 12.4% — C2,C6
4. 提交附匿名代码仓库（训练/评测/预处理脚本+checkpoint+requirements）+ 完整参考文献 — C4,C5

## P1（应改）
5. 消融扩到 ≥3 数据集 + 分解粒度/融合方式敏感性 + w_k 权重分析 — C7
6. 重写相关工作：诚实定位为 Autoformer/DLinear 分解范式延伸，补 TimesNet/Pyraformer/Crossformer；删除"现有方法单一尺度"strawman — C8
7. 补方法细节（尺度偏置定义、融合公式、超参搜索表、硬件、参数量与基线对比）— C10
8. 补训练收敛证据（loss 曲线/early stopping/lr scheduler），论证 10 epoch 充分性 — C9

## P2（建议）
9. 降级因果表述（"证明是关键"→"实验表明有助于"）
10. 效率对比补训练成本/显存，与基线参数量对照
