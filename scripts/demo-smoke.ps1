#Requires -Version 5.1
<#
.SYNOPSIS
  Offline public smoke check for PaperSwarm.
.DESCRIPTION
  Checks the sanitized cached demo. It does not call LLMs, EvoMap, or any
  external service.
#>
$ErrorActionPreference = 'Continue'
$repo = (Resolve-Path "$PSScriptRoot\..").Path
Set-Location $repo

$run = 'runs\demo'
$files = @(
  'README.md',
  'trace.json',
  'resources\paper_draft.example.md',
  "$run\structure\reviewer_set.json",
  "$run\structure\paper_structure.md",
  "$run\review_editor\review_editor.md",
  "$run\review_method\review_method.md",
  "$run\review_domain\review_domain.md",
  "$run\review_devil\review_devil.md",
  "$run\review_ethicist\review_ethicist.md",
  "$run\review_statistician\review_statistician.md",
  "$run\conflict\conflict_report.md",
  "$run\conflict\author_resolution.md",
  "$run\advice\revision_plan.md",
  "$run\revise\paper_revised.md",
  "$run\revise\revise_report.md",
  "$run\archive\review_archive.md",
  "$run\publish\gep_bundle_preview.md",
  "$run\publish\publish_payload.json",
  "$run\publish\gep_bundle.json"
)

$fail = 0
function Check($ok, $name, $detail) {
  if($ok) {
    Write-Host ("[PASS] {0} {1}" -f $name,$detail) -ForegroundColor Green
  } else {
    Write-Host ("[FAIL] {0} {1}" -f $name,$detail) -ForegroundColor Red
    $script:fail++
  }
}

foreach($f in $files) {
  Check (Test-Path $f) 'file' $f
}

if(Get-Command node -ErrorAction SilentlyContinue) {
  $jsons = @(
    'trace.json',
    "$run\structure\reviewer_set.json",
    "$run\publish\gep_bundle.json",
    "$run\publish\publish_payload.json",
    'resources\schema\events.schema.json',
    'resources\schema\demo.events.json'
  )
  foreach($j in $jsons) {
    if(Test-Path $j) {
      $out = (& node -e "JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'))" $j 2>&1 | Out-String).Trim()
      Check ($LASTEXITCODE -eq 0) 'json' $j
      if($LASTEXITCODE -ne 0 -and $out) { Write-Host $out -ForegroundColor DarkRed }
    }
  }

  $out = (& node steps\publish\scripts\validate_review.js $run 2>&1 | Out-String).Trim()
  Check ($LASTEXITCODE -eq 0) 'review-validate' 'review reports match reviewer_set roles'
  if($LASTEXITCODE -ne 0 -and $out) { Write-Host $out -ForegroundColor DarkRed }
} else {
  Check $false 'node' 'node not on PATH; cannot validate JSON or review reports'
}

if(Get-Command uv -ErrorAction SilentlyContinue) {
  $out = (& uv run python steps\publish\scripts\gep_bundle.py validate "$run\publish\gep_bundle.json" 2>&1 | Out-String).Trim()
  Check ($LASTEXITCODE -eq 0) 'gep-bundle' 'GEP bundle validates'
  if($LASTEXITCODE -ne 0 -and $out) { Write-Host $out -ForegroundColor DarkRed }
} else {
  Check $false 'uv' 'uv not on PATH; cannot validate Python helper'
}

$conflict = Join-Path $run 'conflict\conflict_report.md'
if(Test-Path $conflict) {
  $txt = Get-Content $conflict -Raw -Encoding UTF8
  Check ($txt -match 'CI|p|statistician|devil') 'demo-hook' 'conflict report contains cross-review terms'
}

if($fail -eq 0) {
  Write-Host "`nPaperSwarm public demo smoke: PASS" -ForegroundColor Cyan
} else {
  Write-Host "`nPaperSwarm public demo smoke: FAIL ($fail)" -ForegroundColor Red
}
exit $fail
