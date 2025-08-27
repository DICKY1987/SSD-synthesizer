<#
  Detects MT4 terminal config path(s) containing MQL4\Files\config.
  Strategy:
    - %APPDATA%\MetaQuotes\Terminal\*\MQL4\Files\config
    - %LOCALAPPDATA%\MetaQuotes\Terminal\*\MQL4\Files\config
    - %PROGRAMFILES%\*\MetaTrader*\MQL4\Files\config
    - %PROGRAMFILES(X86)%\*\MetaTrader*\MQL4\Files\config
  Prints the first path found (or all with -All). With -UpdateJson, writes it into reentry_pack_config.json.
#>
param(
  [switch]$All,
  [switch]$UpdateJson,
  [string]$ConfigJson = ".\reentry_pack_config.json"
)
$candidates = @()
$roots = @(
  (Join-Path $env:APPDATA       "MetaQuotes\Terminal"),
  (Join-Path $env:LOCALAPPDATA  "MetaQuotes\Terminal"),
  $env:PROGRAMFILES,
  ${env:ProgramFiles(x86)}
) | Where-Object { $_ -and (Test-Path $_) }

foreach ($root in $roots) {
  try {
    $paths = Get-ChildItem -Path $root -Recurse -Directory -ErrorAction SilentlyContinue | ForEach-Object {
      $cfg = Join-Path $_.FullName "MQL4\Files\config"
      if (Test-Path $cfg) { $cfg }
    }
    if ($paths) { $candidates += $paths }
  } catch {}
}

$candidates = $candidates | Sort-Object -Unique
if (-not $candidates) {
  Write-Error "No MT4 config directories found."
  exit 1
}

if ($All) {
  $candidates | ForEach-Object { Write-Host $_ }
} else {
  $chosen = $candidates[0]
  Write-Host $chosen
  if ($UpdateJson) {
    if (-not (Test-Path $ConfigJson)) { throw "Config JSON not found: $ConfigJson" }
    $cfg = Get-Content $ConfigJson -Raw | ConvertFrom-Json
    $cfg.paths.config_root = $chosen
    $cfg | ConvertTo-Json -Depth 10 | Out-File -FilePath $ConfigJson -Encoding utf8
    Write-Host "Updated config_root in $ConfigJson"
  }
}
