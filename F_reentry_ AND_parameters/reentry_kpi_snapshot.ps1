param(
      [string]$DbPath     = "C:\FX\data	rades.db",
      [string]$SQLiteExe  = "sqlite3.exe",
      [string]$OutDir     = "C:\FXeports\weekly",
      [string]$Symbols    = "EURUSD,GBPUSD,USDJPY",
      [switch]$WhatIf
    )

    function Ensure-Dir($p) { if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force -Path $p | Out-Null } }
    Ensure-Dir $OutDir

    $symbols = @()
    foreach ($s in ($Symbols -split ",")) { $t = $s.Trim(); if ($t) { $symbols += $t.ToUpper() } }

    foreach ($sym in $symbols) {
      $viewExec  = "v_reentry_execs_enriched_{0}" -f $sym
      $viewKPIs  = "v_reentry_action_kpis_{0}" -f $sym

      $out1 = Join-Path $OutDir ("{0}_reentry_execs_enriched.csv" -f $sym)
      $out2 = Join-Path $OutDir ("{0}_reentry_action_kpis.csv" -f $sym)

      $q1 = ".headers on
.mode csv
SELECT * FROM {0};" -f $viewExec
      $q2 = ".headers on
.mode csv
SELECT * FROM {0};" -f $viewKPIs

      if ($WhatIf) {
        Write-Host "[DRY] Export $viewExec -> $out1"
        Write-Host "[DRY] Export $viewKPIs -> $out2"
      } else {
        & $SQLiteExe $DbPath $q1 | Out-File -FilePath $out1 -Encoding utf8
        & $SQLiteExe $DbPath $q2 | Out-File -FilePath $out2 -Encoding utf8
      }
    }

    # Optionally: combine summary
    $summary = Join-Path $OutDir "SUMMARY.txt"
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "Weekly KPI snapshot generated at $ts" | Out-File -FilePath $summary -Encoding utf8
    foreach ($sym in $symbols) {
      $p = Join-Path $OutDir ("{0}_reentry_action_kpis.csv" -f $sym)
      " - $sym: $p" | Add-Content -Path $summary
    }
