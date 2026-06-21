#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEP bundle 确定性工具 —— canonical JSON + SHA-256 + 结构校验。

stdlib only（json + hashlib），无第三方依赖，不引入 venv/pip。
PaperSwarm publish step 生成 GEP bundle 后调用本脚本做确定性后处理：
LLM 生成资产内容（语义），本脚本保证 hash/校验的确定性（LLM 算 hash 会错）。

用法:
  python3 gep_bundle.py seal <bundle.json>      # 校验结构 + 算 canonical hash + 回填 bundle_hash + 写回
  python3 gep_bundle.py validate <bundle.json>  # 只校验结构，不改文件，打印报告

退出码: 0=通过, 1=校验失败/出错, 2=用法错误。
"""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

ASSET_TYPES = {"Gene", "Capsule", "EvolutionEvent"}

# 每类资产的必需顶层字段（PRD §6.2）
REQUIRED_FIELDS = {
    "Gene": ["type", "id", "version", "meta", "category", "tags",
             "trigger", "validation", "blast_radius", "outcome"],
    "Capsule": ["type", "id", "gene_id", "version", "meta", "tags", "content"],
    "EvolutionEvent": ["type", "id", "gene_id", "capsule_id", "version",
                       "meta", "event_type", "outcome", "details"],
}

GENE_CATEGORIES = {"repair", "optimize"}


def canonical_json(obj) -> str:
    """所有层级 key 递归排序的紧凑 JSON（EvoMap canonical 规范）。"""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def compute_bundle_hash(bundle: dict) -> str:
    """对 bundle 除 bundle_hash 外的内容算 sha256（排除自身避免自指循环）。"""
    payload = {k: v for k, v in bundle.items() if k != "bundle_hash"}
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return "sha256:" + digest


def _get(obj, *path):
    """从嵌套 dict 取原始值（任意类型），取不到返回 None。"""
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def _num(obj, *path, default=None):
    """从嵌套 dict 取数值，取不到/非数值返回 default。"""
    v = _get(obj, *path)
    return v if isinstance(v, (int, float)) else default


def validate(bundle) -> tuple:
    """校验 bundle 结构 + GEP 硬门槛，返回 (ok, errors)。"""
    errors = []
    if not isinstance(bundle, dict):
        return False, ["bundle 不是 JSON 对象"]

    assets = bundle.get("assets")
    if not isinstance(assets, list) or len(assets) == 0:
        return False, ["bundle.assets 缺失或为空（必须含 Gene+Capsule+EvolutionEvent）"]

    found = {}
    for i, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append("asset[%d] 不是 JSON 对象" % i)
            continue
        t = asset.get("type")
        if t not in ASSET_TYPES:
            errors.append("asset[%d] type=%r 不在 %s" % (i, t, sorted(ASSET_TYPES)))
            continue
        if t in found:
            errors.append("asset[%d] 重复的 type=%s" % (i, t))
        found[t] = asset

        missing = [f for f in REQUIRED_FIELDS[t] if f not in asset]
        if missing:
            errors.append("asset[%d] (%s) 缺字段: %s" % (i, t, missing))

    missing_types = ASSET_TYPES - set(found)
    if missing_types:
        errors.append("缺资产类型: %s" % sorted(missing_types))

    # Gene 硬门槛：validation 至少 1 条 >= 10 字符；category 合法
    gene = found.get("Gene")
    if gene:
        if gene.get("category") not in GENE_CATEGORIES:
            errors.append("Gene.category=%r 不在 %s" % (gene.get("category"), sorted(GENE_CATEGORIES)))
        val = gene.get("validation")
        ok_val = isinstance(val, list) and any(
            isinstance(s, str) and len(s) >= 10 for s in val)
        if not ok_val:
            errors.append("Gene.validation 需至少 1 条 >= 10 字符的命令")

    # Capsule 硬门槛：content.outcome.score >= 0.7；blast_radius.files>0 且 lines>0
    cap = found.get("Capsule")
    if cap:
        score = _num(cap, "content", "outcome", "score", default=-1)
        if score < 0.7:
            errors.append("Capsule.content.outcome.score=%s < 0.7（硬门槛）" % score)
        # blast_radius.files 在 PRD §6.2 里是文件名数组（取长度）；lines 是数值
        bf_raw = _get(cap, "content", "blast_radius", "files")
        bf = len(bf_raw) if isinstance(bf_raw, list) else (bf_raw if isinstance(bf_raw, (int, float)) else 0)
        bl_raw = _get(cap, "content", "blast_radius", "lines")
        bl = bl_raw if isinstance(bl_raw, (int, float)) else 0
        if not (bf > 0 and bl > 0):
            errors.append("Capsule.content.blast_radius files=%s/lines=%s 需 > 0（硬门槛，files 为数组取长度）" % (bf, bl))

    return len(errors) == 0, errors


def _report(ok, errors, bundle_hash=None):
    print("✅ PASS" if ok else "❌ FAIL")
    if bundle_hash:
        print("bundle_hash: %s" % bundle_hash)
    for e in errors:
        print("  - %s" % e)


def main(argv):
    if len(argv) != 3 or argv[1] not in ("seal", "validate"):
        print(__doc__)
        return 2
    cmd, path = argv[1], argv[2]
    p = Path(path)
    try:
        bundle = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("❌ 读取/解析失败: %s" % e)
        return 1

    ok, errors = validate(bundle)
    if cmd == "validate":
        _report(ok, errors)
        return 0 if ok else 1

    # seal: 校验过才回填 hash
    if not ok:
        _report(False, errors)
        print("（校验未过，未回填 hash）")
        return 1
    h = compute_bundle_hash(bundle)
    bundle["bundle_hash"] = h
    p.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    _report(True, [], bundle_hash=h)
    print("已写回 %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
