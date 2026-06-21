#!/usr/bin/env node
// -*- coding: utf-8 -*-
// PaperSwarm 评审产物校验脚本（EvoMap Gene.validation 用）。
// 校验一次 run 的评审报告：存在、非空、含评分。支持可插拔角色池——
// 优先读 structure/reviewer_set.json 的 roles 确定参评角色；无则扫描所有 review_* 目录。
// sentinel 文件（未被选中的角色产出 "N/A — ..."）在 fallback 模式下跳过。
// 用法: node validate_review.js <run_dir>
// 退出码: 0=通过, 1=校验失败, 2=用法错误。

const fs = require("fs");
const path = require("path");

// 评分关键字：中文「评分/分」或英文 score/百分制
const SCORE_RE = /(评分|分|\bscore\b|\/10|\/100)/i;
const MIN_LEN = 50;

// sentinel 检测：未选中角色产出 "N/A — 本类型无需 X 评审"
function isSentinel(txt) {
  const head = txt.trim().slice(0, 80);
  return /^N\/A/.test(head) || /无需.*评审/.test(head);
}

function main(argv) {
  if (argv.length !== 1) {
    console.error("用法: node validate_review.js <run_dir>");
    return 2;
  }
  const runDir = argv[0];
  if (!fs.existsSync(runDir) || !fs.statSync(runDir).isDirectory()) {
    console.error(`❌ run 目录不存在: ${runDir}`);
    return 1;
  }

  // 1. 优先读 reviewer_set.json 确定 roles
  const setPath = path.join(runDir, "structure", "reviewer_set.json");
  let roles = null;
  if (fs.existsSync(setPath)) {
    try {
      const set = JSON.parse(fs.readFileSync(setPath, "utf-8"));
      if (Array.isArray(set.roles) && set.roles.length > 0) roles = set.roles;
    } catch (e) {
      console.error(`⚠ reviewer_set.json 解析失败，回退扫描全部 review_* 目录: ${e.message}`);
    }
  }

  // 2. 确定要校验的 review 文件列表
  const targets = [];
  if (roles) {
    for (const role of roles) {
      targets.push({ role, rel: `review_${role}/review_${role}.md` });
    }
  } else {
    const entries = fs.readdirSync(runDir);
    for (const d of entries) {
      if (!/^review_/.test(d)) continue;
      if (!fs.statSync(path.join(runDir, d)).isDirectory()) continue;
      const f = `${d}/${d}.md`;
      if (fs.existsSync(path.join(runDir, f))) {
        targets.push({ role: d.replace(/^review_/, ""), rel: f });
      }
    }
  }

  if (targets.length === 0) {
    console.error("❌ 未找到任何评审报告（无 reviewer_set.roles 也无 review_* 目录）");
    return 1;
  }

  // 3. 校验
  const errors = [];
  let ok = 0;
  let skipped = 0;
  for (const t of targets) {
    const p = path.join(runDir, t.rel);
    if (!fs.existsSync(p)) {
      errors.push(`缺失: ${t.rel}`);
      continue;
    }
    const txt = fs.readFileSync(p, "utf-8");
    if (isSentinel(txt)) {
      // roles 内的角色不应是 sentinel（说明组队决策与实际产出矛盾）
      if (roles) {
        errors.push(`${t.rel}: 在 reviewer_set.roles 内却是 sentinel（组队与实际不符）`);
      } else {
        skipped++;
      }
      continue;
    }
    if (txt.length < MIN_LEN) {
      errors.push(`${t.rel}: 内容过短 (${txt.length} < ${MIN_LEN})`);
      continue;
    }
    if (!SCORE_RE.test(txt)) {
      errors.push(`${t.rel}: 缺评分关键字`);
      continue;
    }
    ok++;
  }

  const total = targets.length;
  if (errors.length === 0) {
    const skipMsg = skipped ? `，跳过 ${skipped} 个 sentinel` : "";
    console.log(`✅ PASS ${ok}/${total} 评审报告完整且含评分 (run: ${path.basename(runDir)}${skipMsg})`);
    return 0;
  }
  console.error(`❌ FAIL ${ok}/${total} 通过`);
  for (const e of errors) console.error(`  - ${e}`);
  return 1;
}

process.exit(main(process.argv.slice(2)));
