#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EvoMap signals 构造器 —— 把 PaperSwarm 评审元数据归一化为 EvoMap memory signals。

⚠ record（archive 后写）与 recall（structure 前读）必须共用本模块，否则 signals
词表不一致 → 召回相似度退化为噪声。本模块是 signals 的唯一来源。

输入字段（experience_update.json 或 reviewer_set.json 都有）:
  paper_type : str   medical-rct / cs-ml-benchmark / education-quasi-experiment / journal-paper
  discipline : str   临床医学（内分泌与代谢） / 计算机科学（机器学习/时序预测） / ...
  method     : str   定量RCT / 定量实证（基准对比+消融） / 定量准实验 / ...
  roles      : list  [editor, method, domain, devil, statistician, ...]

输出:
  ["paper-review", "discipline-{disc}", "method-{m}", "type-{paper_type}",
   "role-{r}", ...]
"""
from __future__ import annotations


def normalize_discipline(paper_type: str = "", discipline: str = "") -> str:
    """paper_type 前缀优先，回退 discipline 中文关键词。→ medical/cs/education/other"""
    pt = (paper_type or "").lower()
    if pt.startswith("medical"):
        return "medical"
    if pt.startswith("cs"):
        return "cs"
    if pt.startswith("education") or pt.startswith("edu"):
        return "education"
    d = discipline or ""
    dl = d.lower()
    if any(k in d for k in ("医学", "临床")) or "medical" in dl:
        return "medical"
    if any(k in d for k in ("计算机", "机器学习", "计算")) or "computer" in dl:
        return "cs"
    if "教育" in d or "education" in dl:
        return "education"
    return "other"


def normalize_method(method: str = "") -> str:
    """中/英 method → 固定词表。顺序敏感：rct/quasi/benchmark 必须先于 quantitative。"""
    m = method or ""
    if any(k in m for k in ("RCT", "rct", "随机对照")):
        return "rct"
    if any(k in m for k in ("准实验", "quasi")):
        return "quasi-experiment"
    if any(k in m for k in ("基准", "benchmark", "消融", "ablation")):
        return "benchmark"
    if any(k in m for k in ("定性", "qualitative")):
        return "qualitative"
    if any(k in m for k in ("混合", "mixed")):
        return "mixed"
    if any(k in m for k in ("定量", "quantitative", "实证")):
        return "quantitative"
    return "unknown"


def build_signals(paper_type: str = "", discipline: str = "",
                  method: str = "", roles=None) -> list:
    """构造 EvoMap memory signals。record 与 recall 共用 → 词表一致。"""
    roles = roles or []
    sigs = [
        "paper-review",
        f"discipline-{normalize_discipline(paper_type, discipline)}",
        f"method-{normalize_method(method)}",
    ]
    if paper_type:
        sigs.append(f"type-{paper_type}")
    for r in roles:
        if r:
            sigs.append(f"role-{r}")
    return sigs


if __name__ == "__main__":
    # 自测：覆盖 4 个真实 run 的字段
    cases = [
        ("medical-rct", "临床医学（内分泌与代谢）", "定量RCT",
         ["editor", "method", "domain", "devil", "statistician", "ethicist"]),
        ("cs-ml-benchmark", "计算机科学（机器学习/时序预测）", "定量实证（基准对比+消融）",
         ["editor", "method", "domain", "devil", "reproducibility"]),
        ("education-quasi-experiment", "教育学（数学教学）", "定量准实验",
         ["editor", "method", "domain", "devil"]),
        ("journal-paper", "education", "quantitative-quasi-experiment",
         ["editor", "method", "domain", "devil"]),
    ]
    for pt, d, m, r in cases:
        print(f"{pt:32s} → {build_signals(pt, d, m, r)}")
