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
$case = 'case-studies\medical-rct-lx204'
$caseCs = 'case-studies\cs-ml-benchmark'
$caseEdu = 'case-studies\education-quasi-experiment'
$experimentRecall = 'experiments\cold-vs-warm-recall'
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
  "$run\publish\gep_bundle.json",
  'integrations\evomap\README.md',
  'integrations\evomap\workflow.md',
  'integrations\evomap\examples\recall_medical_rct.sanitized.json',
  'docs\evidence\README.md',
  'docs\evidence\non-consensus-evidence.md',
  'docs\evidence\schema-gap-report.md',
  "$case\README.md",
  "$case\input\paper_draft.medical.md",
  "$case\run\structure\reviewer_set.json",
  "$case\run\conflict\conflict_report.md",
  "$case\run\advice\revision_plan.md",
  "$case\run\revise\revise_report.md",
  "$case\run\archive_review_archive.md",
  "$case\run\gep_bundle.json",
  "$case\p1-audit\events.demo.json",
  'case-studies\README.md',
  "$caseCs\README.md",
  "$caseCs\run\structure\reviewer_set.json",
  "$caseCs\run\review_reproducibility\review_reproducibility.md",
  "$caseCs\run\conflict\conflict_report.md",
  "$caseCs\run\gep_bundle.json",
  "$caseEdu\README.md",
  "$caseEdu\run\structure\paper_structure.md",
  "$caseEdu\run\conflict\conflict_report.md",
  "$caseEdu\run\revise\worker-round1.md",
  "$caseEdu\run\revise\verifier-round1.md",
  "$caseEdu\run\revise\worker-round2.md",
  "$caseEdu\run\revise\verifier-round2.md",
  "$caseEdu\run\revise\paper_revised.md",
  "$caseEdu\run\revise\revise_report.md",
  "$caseEdu\run\gep_bundle.json",
  "$experimentRecall\README.md",
  "$experimentRecall\comparison.md",
  "$experimentRecall\cold\reviewer_set.json",
  "$experimentRecall\cold\review_statistician.md",
  "$experimentRecall\warm\reviewer_set.json",
  "$experimentRecall\warm\review_statistician.md",
  "$experimentRecall\examples\warm_recall.sanitized.json"
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
    "$case\run\structure\reviewer_set.json",
    "$case\run\gep_bundle.json",
    "$case\p1-audit\events.demo.json",
    "$caseCs\run\structure\reviewer_set.json",
    "$caseCs\run\gep_bundle.json",
    "$caseEdu\run\gep_bundle.json",
    'integrations\evomap\examples\recall_medical_rct.sanitized.json',
    "$experimentRecall\cold\reviewer_set.json",
    "$experimentRecall\warm\reviewer_set.json",
    "$experimentRecall\examples\warm_recall.sanitized.json",
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

  $out = (& uv run python steps\publish\scripts\gep_bundle.py validate "$case\run\gep_bundle.json" 2>&1 | Out-String).Trim()
  Check ($LASTEXITCODE -eq 0) 'case-gep-bundle' 'medical RCT case GEP bundle validates'
  if($LASTEXITCODE -ne 0 -and $out) { Write-Host $out -ForegroundColor DarkRed }

  $out = (& uv run python steps\publish\scripts\gep_bundle.py validate "$caseCs\run\gep_bundle.json" 2>&1 | Out-String).Trim()
  Check ($LASTEXITCODE -eq 0) 'case-cs-gep-bundle' 'CS case GEP bundle validates'
  if($LASTEXITCODE -ne 0 -and $out) { Write-Host $out -ForegroundColor DarkRed }

  $out = (& uv run python steps\publish\scripts\gep_bundle.py validate "$caseEdu\run\gep_bundle.json" 2>&1 | Out-String).Trim()
  Check ($LASTEXITCODE -eq 0) 'case-edu-gep-bundle' 'education case GEP bundle validates'
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
