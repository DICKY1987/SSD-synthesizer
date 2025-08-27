param(
  [string]$ProfilesRoot = "C:\FX\ReentryProfiles",     # e.g., C:\FX\ReentryProfiles\<persona>\<SYMBOL>_reentry.csv
  [string]$ConfigRoot   = "C:\MT4\MQL4\Files\config",  # EA reads <SYMBOL>_reentry.csv from here
  [string]$Persona = "",                                # e.g., conservative|moderate|aggressive (overrides cycle)
  [string]$PersonaCycle = "conservative,moderate,aggressive", # used if -Persona not set
  [string]$Symbols = "EURUSD,GBPUSD,USDJPY",            # comma-separated list
  [switch]$WhatIf,                                      # dry-run copy
  [string]$LogPath = "C:\FX\logseentry_profile_rotate.log"
)

# Map day-of-week -> persona if -Persona empty (customize as needed)
$CycleMap = @{
  "Monday"    = "conservative"
  "Tuesday"   = "moderate"
  "Wednesday" = "aggressive"
  "Thursday"  = "conservative"
  "Friday"    = "moderate"
  "Saturday"  = "conservative"  # markets closed: set a conservative/no_reentry template if desired
  "Sunday"    = "moderate"
}

if (-not $Persona) {
  $today = (Get-Date).DayOfWeek.ToString()
  $Persona = $CycleMap[$today]
  if (-not $Persona) {
    $Persona = ($PersonaCycle -split ",")[0].Trim()
  }
}

$symbols = @()
foreach ($s in ($Symbols -split ",")) { $t = $s.Trim(); if ($t) { $symbols += $t.ToUpper() } }

New-Item -ItemType Directory -Force -Path (Split-Path $LogPath) | Out-Null
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LogPath -Value "[$time] Persona=$Persona Symbols=$($symbols -join ',')"

foreach ($sym in $symbols) {
  $src = Join-Path (Join-Path $ProfilesRoot $Persona) ("{0}_reentry.csv" -f $sym)
  $dst = Join-Path $ConfigRoot ("{0}_reentry.csv" -f $sym)
  if (-not (Test-Path $src)) {
    $msg = "Source profile not found: $src"
    Write-Warning $msg
    Add-Content -Path $LogPath -Value $msg
    continue
  }
  $action = "Copy `"$src`" -> `"$dst`""
  if ($WhatIf) {
    Write-Host "[DRY] $action"
    Add-Content -Path $LogPath -Value "[DRY] $action"
  } else {
    New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
    Copy-Item -Force -Path $src -Destination $dst
    Write-Host $action
    Add-Content -Path $LogPath -Value $action
  }
}
