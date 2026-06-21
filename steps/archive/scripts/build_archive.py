#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地经验库合并器（P0a）—— 把本次 run 的 experience_update.json 合并进 experience.json。

⚠ 纯本地、零网络、零外部依赖（skeptic 要求 P0a 必须零外部风险，是离线兜底能演
「经验进化」而非「跑完流程」的前提）。EvoMap 回写由 archive step 另调 evomap_record.py。

修复 audit 实证的致命缺口：归档曾只停留在 SOP 描述，没有实际写入本地经验库 →
experience.json entries 永远空 → 读端 structure/review/conflict 读空库 → 跨论文
经验复用实际为零。本脚本打通本地归档与经验复用链。

用法:
  python3 build_archive.py <experience_update.json> [--exp <experience.json>]

默认 experience.json = <root>/resources/knowledge/experience.json（按脚本位置定位）。
去重 by run_id：重跑同一 run 时覆盖旧 entry，不重复累积。

退出码: 0=合并成功; 1=IO/格式错; 2=用法错。
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))  # scripts→archive→steps→root
DEFAULT_EXP = os.path.join(ROOT, "resources", "knowledge", "experience.json")


def make_entry(exp):
    """experience_update → experience.json 的一条 entry。兼容旧格式（无 roles_used/lesson）。"""
    roles = exp.get("roles_used") or list((exp.get("agent_reliability") or {}).keys())
    return {
        "run_id": exp.get("run_id", "unknown"),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "paper_type": exp.get("paper_type", ""),
        "discipline": exp.get("discipline", ""),
        "method": exp.get("method", ""),
        "roles": roles,
        "high_frequency_issues": exp.get("high_frequency_issues", []),
        "agent_reliability": exp.get("agent_reliability", {}),
        "conflict_patterns": exp.get("conflict_patterns", []),
        "lesson": exp.get("lesson", ""),
    }


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    update_path = argv[1]
    exp_path = DEFAULT_EXP
    for a in argv[2:]:
        if a.startswith("--exp="):
            exp_path = a.split("=", 1)[1]

    try:
        exp = json.load(open(update_path, encoding="utf-8"))
    except Exception as e:
        print(f"[build_archive] ERROR 读取 {update_path} 失败: {e}"); return 1
    try:
        lib = json.load(open(exp_path, encoding="utf-8"))
    except FileNotFoundError:
        lib = {"version": "0.1.0", "description": "PaperSwarm 本地经验库", "entries": []}
    except Exception as e:
        print(f"[build_archive] ERROR 读取 {exp_path} 失败: {e}"); return 1

    run_id = exp.get("run_id", "unknown")
    entries = [e for e in lib.get("entries", []) if e.get("run_id") != run_id]  # 去重
    action = "覆盖" if len(entries) < len(lib.get("entries", [])) else "新增"
    entry = make_entry(exp)
    entries.append(entry)
    lib["entries"] = entries

    try:
        json.dump(lib, open(exp_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[build_archive] ERROR 写回 {exp_path} 失败: {e}"); return 1

    print(f"[build_archive] {action} entry run_id={run_id} → {exp_path}")
    print(f"[build_archive] entries 总数: {len(entries)} | disciplines: "
          f"{sorted({e['discipline'][:12] for e in entries})}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
