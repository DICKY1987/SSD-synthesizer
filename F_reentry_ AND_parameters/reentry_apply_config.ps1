param(
  [string]$ConfigPath = ".\reentry_pack_config.json"
)
if (-not (Test-Path $ConfigPath)) {
  throw "Config not found: $ConfigPath"
}
$cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$scriptsDir = $cfg.paths.scripts_dir
New-Item -ItemType Directory -Force -Path $scriptsDir | Out-Null

# Copy required scripts (assumes current files are next to this script)
Copy-Item -Force -Path ".\sqlite_reentry_create_views.py" -Destination (Join-Path $scriptsDir "sqlite_reentry_create_views.py")
Copy-Item -Force -Path ".\reentry_profile_rotate.ps1"    -Destination (Join-Path $scriptsDir "reentry_profile_rotate.ps1")
Copy-Item -Force -Path ".\reentry_kpi_snapshot.ps1"      -Destination (Join-Path $scriptsDir "reentry_kpi_snapshot.ps1")

# Render XML tasks from config
python ".\render_reentry_tasks.py" $ConfigPath "."
Write-Host "Applied config. Import the generated XML tasks in Task Scheduler."
