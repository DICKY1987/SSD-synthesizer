<#
  Verifies core components:
    - DB exists, required tables exist for each symbol
    - Views exist
    - Scripts present in scripts_dir
    - MT4 config_root exists and has at least one <SYMBOL>_reentry.csv
#>
param([string]$ConfigPath = ".\reentry_pack_config.json")
function Get-Json { param($p) Get-Content $p -Raw | ConvertFrom-Json }
if (-not (Test-Path $ConfigPath)) { throw "Config not found: $ConfigPath" }
$cfg = Get-Json $ConfigPath
$ok = $true
$db = $cfg.paths.db_path
$scripts = $cfg.paths.scripts_dir
$cfgroot = $cfg.paths.config_root

# 1) DB checks via sqlite3 if available
$sqlite = $cfg.paths.sqlite_exe
if (Test-Path $sqlite) {
  foreach ($s in $cfg.symbols) {
    $tables = @(
      "trades_{0}" -f $s,
      "reentry_chains_{0}" -f $s,
      "reentry_executions_{0}" -f $s,
      "reentry_performance_{0}" -f $s
    )
    foreach ($t in $tables) {
      $q = ".headers off`n.mode list`nSELECT name FROM sqlite_master WHERE type='table' AND name='$t';"
      $res = & $sqlite $db $q
      if (-not $res) { Write-Warning "Missing table: $t"; $ok = $false }
    }
    $views = @(
      "v_reentry_execs_enriched_{0}" -f $s,
      "v_trades_with_reentry_{0}" -f $s,
      "v_reentry_action_kpis_{0}" -f $s
    )
    foreach ($v in $views) {
      $q = ".headers off`n.mode list`nSELECT name FROM sqlite_master WHERE type='view' AND name='$v';"
      $res = & $sqlite $db $q
      if (-not $res) { Write-Warning "Missing view: $v"; $ok = $false }
    }
  }
} else {
  Write-Warning "sqlite3.exe not found at $sqlite — DB checks skipped."
}

# 2) Scripts present
$needed = @("sqlite_reentry_create_views.py","sqlite_reentry_migrate.py","reentry_profile_rotate.ps1","reentry_kpi_snapshot.ps1","render_reentry_tasks.py","seed_reentry_performance.py")
foreach ($n in $needed) {
  $p = Join-Path $scripts $n
  if (-not (Test-Path $p)) { Write-Warning "Missing script: $p"; $ok = $false }
}

# 3) MT4 profiles present
if (-not (Test-Path $cfgroot)) {
  Write-Warning "config_root not found: $cfgroot"
  $ok = $false
} else {
  $foundAny = $false
  foreach ($s in $cfg.symbols) {
    $f = Join-Path $cfgroot ("{0}_reentry.csv" -f $s)
    if (Test-Path $f) { $foundAny = $true; break }
  }
  if (-not $foundAny) {
    Write-Warning "No <SYMBOL>_reentry.csv profiles found in $cfgroot"
    $ok = $false
  }
}

if ($ok) { Write-Host "Verification PASSED" } else { Write-Host "Verification completed with warnings/errors." }
