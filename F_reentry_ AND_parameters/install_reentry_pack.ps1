<#
  End-to-end installer:
    1) Ensure JSON config present (or abort).
    2) Optionally autodetect MT4 config path and update JSON.
    3) Copy scripts to scripts_dir.
    4) Run DB migrations, create views, seed KPI rows.
    5) Render Task XMLs based on JSON.
    6) Optional: register tasks with schtasks.exe (/XML).
#>
param(
  [string]$ConfigPath = ".\reentry_pack_config.json",
  [switch]$AutoDetectMT4,
  [switch]$RegisterTasks,          # Use schtasks.exe to register tasks (requires admin or proper creds)
  [string]$TaskPrefix = "Reentry", # Task name prefix
  [string]$RunUser = "",           # When registering tasks
  [string]$RunPass = ""            # If empty, schtasks will prompt
)

function Get-Json { param($p) Get-Content $p -Raw | ConvertFrom-Json }
if (-not (Test-Path $ConfigPath)) { throw "Config not found: $ConfigPath" }
$cfg = Get-Json $ConfigPath
$scriptsDir = $cfg.paths.scripts_dir
New-Item -ItemType Directory -Force -Path $scriptsDir | Out-Null

if ($AutoDetectMT4 -and [string]::IsNullOrWhiteSpace($cfg.paths.config_root)) {
  Write-Host "Autodetecting MT4 config path..."
  $detected = powershell -NoProfile -ExecutionPolicy Bypass -File ".\detect_mt4_config.ps1"
  if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($detected)) {
    $cfg.paths.config_root = $detected.Trim()
    $cfg | ConvertTo-Json -Depth 10 | Out-File -FilePath $ConfigPath -Encoding utf8
    Write-Host "Set config_root = $($cfg.paths.config_root)"
  } else {
    Write-Warning "Autodetection failed; using existing config_root: $($cfg.paths.config_root)"
  }
}

# Copy scripts
Copy-Item -Force -Path ".\sqlite_reentry_create_views.py" -Destination (Join-Path $scriptsDir "sqlite_reentry_create_views.py")
Copy-Item -Force -Path ".\sqlite_reentry_migrate.py"      -Destination (Join-Path $scriptsDir "sqlite_reentry_migrate.py")
Copy-Item -Force -Path ".\reentry_profile_rotate.ps1"     -Destination (Join-Path $scriptsDir "reentry_profile_rotate.ps1")
Copy-Item -Force -Path ".\reentry_kpi_snapshot.ps1"       -Destination (Join-Path $scriptsDir "reentry_kpi_snapshot.ps1")
Copy-Item -Force -Path ".\render_reentry_tasks.py"        -Destination (Join-Path $scriptsDir "render_reentry_tasks.py")
Copy-Item -Force -Path ".\seed_reentry_performance.py"    -Destination (Join-Path $scriptsDir "seed_reentry_performance.py")

# Migrate DB
$syms = ($cfg.symbols) -join ','
Write-Host "Migrating DB for symbols: $syms"
python (Join-Path $scriptsDir "sqlite_reentry_migrate.py") --db $cfg.paths.db_path --symbols $syms

# Create views
Write-Host "Creating analytics views..."
python (Join-Path $scriptsDir "sqlite_reentry_create_views.py") --db $cfg.paths.db_path --symbols $syms

# Seed performance rows
Write-Host "Seeding performance rows..."
python (Join-Path $scriptsDir "seed_reentry_performance.py") --db $cfg.paths.db_path --symbols $syms

# Render Tasks
Write-Host "Rendering Task XMLs..."
python (Join-Path $scriptsDir "render_reentry_tasks.py") $ConfigPath $PSScriptRoot

if ($RegisterTasks) {
  Write-Host "Registering tasks from XML via schtasks.exe..."
  $rotateXml = Join-Path $PSScriptRoot "Task_ProfileRotate.xml"
  $kpiXml    = Join-Path $PSScriptRoot "Task_KPIWeekly.xml"
  $tn1 = "$TaskPrefix-ProfileRotate"
  $tn2 = "$TaskPrefix-KPIWeekly"

  if ([string]::IsNullOrWhiteSpace($RunUser)) {
    schtasks /Create /TN $tn1 /XML $rotateXml /F
    schtasks /Create /TN $tn2 /XML $kpiXml /F
  } else {
    if ([string]::IsNullOrWhiteSpace($RunPass)) {
      schtasks /Create /TN $tn1 /XML $rotateXml /RU $RunUser /F
      schtasks /Create /TN $tn2 /XML $kpiXml /RU $RunUser /F
    } else {
      schtasks /Create /TN $tn1 /XML $rotateXml /RU $RunUser /RP $RunPass /F
      schtasks /Create /TN $tn2 /XML $kpiXml /RU $RunUser /RP $RunPass /F
    }
  }
}

Write-Host "Install complete."
