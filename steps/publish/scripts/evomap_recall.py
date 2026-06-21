#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EvoMap memory/recall 客户端 —— 评审前召回历史评审经验，注入本次 review prompt。

与 evomap_record.py 对称（memory 读端）。stdlib only，~/.evomap/ 读凭据。

⚠ 扁平 body（{sender_id, signals, limit}），非 gep-a2a envelope。实测 recall 返回
matches[] 含 similarity/decay_factor/weighted_score/outcome.note。

用法:
  python3 evomap_recall.py <reviewer_set.json> [--out <evomap_recall.json>] [--limit 5]

退出码: 0=有或无命中 OR 网络降级（均不阻断评审）; 2=用法错。
structure step 评审前调用：命中则把 injection_text 注入各 review prompt；网络失败
则写空 matches，structure 回退纯本地 experience.json。
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


def extract_recall_fields(rs):
    return {
        "paper_type": rs.get("paper_type", ""),
        "discipline": rs.get("discipline", ""),
        "method": rs.get("method", ""),
        "roles": rs.get("roles") or [],
    }


def build_injection(matches):
    """把 top matches 拼成可注入 prompt 的可读文本。"""
    if not matches:
        return ""
    lines = []
    for m in matches[:3]:
        note = (m.get("outcome") or {}).get("note", "")
        sim = m.get("similarity", 0)
        if note:
            lines.append(f"- [相似度 {sim}] {note[:200]}")
    return ("【EvoMap 进化记忆·跨论文召回】历史同类论文评审经验:\n" + "\n".join(lines)) if lines else ""


def _write_empty(out_path, signals, reason):
    json.dump({
        "source": "evomap_memory",
        "query_signals": signals,
        "total_candidates": 0,
        "matches": [],
        "injection_text": "",
        "offline_reason": reason,
    }, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    path = argv[1]
    out_path, limit = None, 5
    for a in argv[2:]:
        if a.startswith("--out="):
            out_path = a.split("=", 1)[1]
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
    if out_path is None:
        out_path = os.path.join(os.path.dirname(os.path.abspath(path)), "evomap_recall.json")

    try:
        rs = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"[recall] ERROR 读取 {path} 失败: {e}（降级，跳过注入）")
        _write_empty(out_path, [], "读取 reviewer_set 失败")
        return 0
    f = extract_recall_fields(rs)
    signals = evomap_signals.build_signals(f["paper_type"], f["discipline"],
                                           f["method"], f["roles"])
    try:
        node_id, secret = load_creds()
        body = json.dumps({"sender_id": node_id, "signals": signals, "limit": limit},
                          ensure_ascii=False).encode()
        req = urllib.request.Request(f"{HUB}/a2a/memory/recall", data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {secret}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        matches = d.get("matches") or []
        slim = [{
            "gene_id": m.get("gene_id"),
            "similarity": m.get("similarity"),
            "weighted_score": m.get("weighted_score"),
            "score": (m.get("outcome") or {}).get("score"),
            "note": (m.get("outcome") or {}).get("note", ""),
            "signals": m.get("signals"),
        } for m in matches]
        result = {
            "source": "evomap_memory",
            "query_signals": signals,
            "total_candidates": d.get("total_candidates", len(matches)),
            "matches": slim,
            "injection_text": build_injection(matches),
        }
        json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[recall] HTTP {r.status} 命中 {len(matches)} 条 → {out_path}")
        for m in slim[:3]:
            print(f"  - sim={m['similarity']} w={m['weighted_score']} | {str(m['note'])[:70]}")
        if not matches:
            print("[recall] （无命中，冷启动或信号过窄）")
        return 0
    except Exception as e:
        print(f"[recall] WARNING 召回失败: {e}（降级，走本地 experience.json）")
        _write_empty(out_path, signals, str(e))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
