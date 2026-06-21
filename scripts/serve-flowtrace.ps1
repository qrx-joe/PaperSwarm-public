#Requires -Version 5.1
<#
.SYNOPSIS
  Start the Flowtrace Web UI for this public PaperSwarm repository.
.DESCRIPTION
  Flowtrace's --scope argument points to the directory that contains trace
  project folders, not the trace project folder itself. This repository contains
  trace.json at its root, so the correct scope is this repository's parent
  directory.

  This script depends on a local Flowtrace CLI installation. It does not bundle
  the Flowtrace Web UI source or binary.
.PARAMETER Port
  Local port to bind. Default: 3001.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\serve-flowtrace.ps1
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\serve-flowtrace.ps1 -Port 3003
#>
param(
  [int]$Port = 3001
)

$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$scope = Split-Path -Parent $repo
$pidFile = Join-Path $PSScriptRoot '.flowtrace.pid'

$cmd = Get-Command flowtrace -ErrorAction SilentlyContinue
if(-not $cmd) {
  $fallback = Join-Path $env:USERPROFILE '.cargo\bin\flowtrace.exe'
  if(Test-Path $fallback) {
    $flowtrace = $fallback
  } else {
    Write-Host 'FAIL: flowtrace CLI is not installed or not on PATH.' -ForegroundColor Red
    Write-Host 'Install Flowtrace first, then rerun this script.' -ForegroundColor DarkGray
    exit 1
  }
} else {
  $flowtrace = $cmd.Source
}

$busy = $false
try {
  if(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction Stop) {
    $busy = $true
  }
} catch {
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect('127.0.0.1', $Port)
    $client.Close()
    $busy = $true
  } catch {
    $busy = $false
  }
}

if($busy) {
  Write-Host "Port $Port is already in use. Open http://127.0.0.1:$Port or pass -Port <other>." -ForegroundColor Yellow
  exit 1
}

$proc = Start-Process -FilePath $flowtrace -ArgumentList @('serve', '--scope', $scope, '--port', $Port) -WorkingDirectory $repo -WindowStyle Hidden -PassThru
Set-Content -Path $pidFile -Value $proc.Id -Encoding ASCII

$ok = $false
for($i = 0; $i -lt 50; $i++) {
  Start-Sleep -Milliseconds 200
  try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/traces" -UseBasicParsing -TimeoutSec 2
    if($response.StatusCode -eq 200 -and $response.Content -match 'paperswarm') {
      $ok = $true
      break
    }
  } catch {}
}

if($ok) {
  Write-Host "Flowtrace UI ready: http://127.0.0.1:$Port" -ForegroundColor Green
  Write-Host "Trace scope: $scope" -ForegroundColor DarkGray
  Write-Host "PID: $($proc.Id) -> $pidFile" -ForegroundColor DarkGray
  Write-Host "Stop: Get-Content $pidFile | ForEach-Object { Stop-Process -Id `$_ }" -ForegroundColor DarkGray
} else {
  Write-Host "WARN: Flowtrace started, but the PaperSwarm trace was not detected within 10 seconds." -ForegroundColor Yellow
  Write-Host "Check http://127.0.0.1:$Port and verify that --scope points to the repository parent: $scope" -ForegroundColor DarkGray
  exit 2
}
