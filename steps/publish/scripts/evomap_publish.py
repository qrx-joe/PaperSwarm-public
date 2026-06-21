#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EvoMap Hub 发送器 —— 把 GEP bundle 发到 EvoMap marketplace。

stdlib only。从 ~/.evomap/ 读凭据（不进 stdout/history）。
用法:
  python3 evomap_publish.py validate <bundle.json>   # dry-run，不存储不扣费
  python3 evomap_publish.py publish  <bundle.json>   # 真发，不可逆外发（candidate 状态）

bundle.json 是 Hub schema 1.5.0 版（含已算好的 asset_id）。
退出码: 0=成功, 1=Hub 拒绝/出错, 2=用法错误。
"""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

HUB = "https://evomap.ai"
UA = "curl/8.7.1"  # Hub 在 Cloudflare 后，python urllib 默认 UA 被 403-1010 拦


def load_creds():
    base = os.path.expanduser("~/.evomap")
    nid = open(f"{base}/node_id", encoding="utf-8-sig").read().strip().lstrip("\ufeff")
    sec = open(f"{base}/node_secret", encoding="utf-8-sig").read().strip().lstrip("\ufeff")
    return nid, sec


def send(endpoint, node_id, secret, assets):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mid = f"msg_{int(time.time()*1000)}_{os.urandom(2).hex()}"
    envelope = {
        "protocol": "gep-a2a", "protocol_version": "1.0.0",
        "message_type": "publish", "message_id": mid,
        "sender_id": node_id, "timestamp": ts,
        "payload": {"assets": assets},
    }
    body = json.dumps(envelope).encode()
    req = urllib.request.Request(f"{HUB}{endpoint}", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {secret}", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main(argv):
    if len(argv) != 3 or argv[1] not in ("validate", "publish"):
        print(__doc__); return 2
    mode, path = argv[1], argv[2]
    bundle = json.load(open(path, encoding="utf-8"))
    assets = bundle["assets"] if isinstance(bundle, dict) and "assets" in bundle else bundle
    node_id, secret = load_creds()
    endpoint = "/a2a/validate" if mode == "validate" else "/a2a/publish"
    code, raw = send(endpoint, node_id, secret, assets)
    print(f"{mode.upper()} HTTP {code}")
    try:
        d = json.loads(raw)
        print(json.dumps(d, ensure_ascii=False, indent=2))
        p = d.get("payload", d)
        ok = (code == 200) and (mode == "validate" and p.get("valid") or mode == "publish")
        return 0 if ok else 1
    except Exception:
        print("body:", raw[:1500].decode("utf-8", "replace"))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
