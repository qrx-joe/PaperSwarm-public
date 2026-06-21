#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EvoMap memory/record 客户端 —— 把本次评审经验回写到 EvoMap 进化记忆。

与 evomap_recall.py 对称（memory 的写/读两端）。stdlib only，从 ~/.evomap/ 读凭据。

⚠ memory API 用扁平 body（{sender_id, signals, ...}），不是 fetch/publish 的 gep-a2a
envelope。本端点 2026-06-18 实测：record 返回 {ok:true, recorded:<id>}，
recall 返回 matches[] 含 similarity/decay_factor/weighted_score。

用法:
  python3 evomap_record.py <experience_update.json>

退出码: 0=成功 OR 网络失败降级（均不阻断 archive 主链）; 2=用法错。
archive step 调用本脚本时，任何失败都只 print warning，不让评审流程挂掉。
"""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error
import evomap_signals

HUB = "https://evomap.ai"
UA = "curl/8.7.1"  # Cloudflare 拦默认 UA（403-1010）


def load_creds():
    base = os.path.expanduser("~/.evomap")
    return (
        open(f"{base}/node_id", encoding="utf-8-sig").read().strip().lstrip("\ufeff"),
        open(f"{base}/node_secret", encoding="utf-8-sig").read().strip().lstrip("\ufeff"),
    )


def compute_score(exp):
    """agent_reliability 各角色 score（0-5）平均后归一化到 0-1。无则默认 0.8。"""
    rel = exp.get("agent_reliability") or {}
    scores = []
    for info in rel.values():
        s = info.get("score") if isinstance(info, dict) else info
        if isinstance(s, (int, float)):
            scores.append(s)
    return round(sum(scores) / len(scores) / 5.0, 3) if scores else 0.8


def build_summary(exp):
    """从 experience_update 提炼可召回的经验摘要（<500 字）。"""
    parts = []
    if exp.get("lesson"):
        parts.append(f"lesson={exp['lesson']}")
    hf = exp.get("high_frequency_issues") or []
    pats = [h.get("pattern", "") for h in hf if isinstance(h, dict) and h.get("pattern")][:3]
    if pats:
        parts.append("高频问题=" + "; ".join(pats))
    rel = exp.get("agent_reliability") or {}
    if rel:
        rel_short = ",".join(f"{r}:{(v.get('score') if isinstance(v, dict) else v)}"
                             for r, v in rel.items())
        parts.append(f"agent_reliability={{{rel_short}}}")
    return " | ".join(parts)[:480]


def extract_record_fields(exp):
    """从 experience_update.json 抽 record 所需字段，兼容旧格式（无 roles_used）。"""
    roles = exp.get("roles_used")
    if not roles:  # 4308 旧格式：从 agent_reliability 的 keys 回退
        roles = list((exp.get("agent_reliability") or {}).keys())
    return {
        "paper_type": exp.get("paper_type", ""),
        "discipline": exp.get("discipline", ""),
        "method": exp.get("method", ""),
        "roles": roles,
        "run_id": exp.get("run_id", "unknown"),
    }


def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    path = argv[1]
    try:
        exp = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"[record] ERROR 读取 {path} 失败: {e}（降级，不阻断）")
        return 0
    f = extract_record_fields(exp)
    signals = evomap_signals.build_signals(f["paper_type"], f["discipline"],
                                           f["method"], f["roles"])
    score = compute_score(exp)
    summary = build_summary(exp)
    gene_id = f"paperswarm-{f['run_id']}"
    try:
        node_id, secret = load_creds()
        body = json.dumps({
            "sender_id": node_id,
            "signals": signals,
            "gene_id": gene_id,
            "status": "success",
            "score": score,
            "summary": summary,
        }, ensure_ascii=False).encode()
        req = urllib.request.Request(f"{HUB}/a2a/memory/record", data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {secret}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
        print(f"[record] HTTP {r.status} gene_id={gene_id} score={score}")
        print(f"[record] signals={signals}")
        try:
            print(json.dumps(json.loads(raw), ensure_ascii=False, indent=2))
        except Exception:
            print("body:", raw[:800].decode("utf-8", "replace"))
        return 0
    except Exception as e:
        print(f"[record] WARNING 回写 EvoMap memory 失败: {e}（降级，经验仅本地沉淀）")
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
