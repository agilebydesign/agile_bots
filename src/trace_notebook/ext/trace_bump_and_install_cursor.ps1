# Bump version, rebuild, and reinstall the Trace Notebook extension
# Usage: .\trace_bump_and_install_cursor.ps1 [patch|minor|major] [-NoReload]
# Default: patch (0.1.0 -> 0.1.1), auto-reloads window
# -NoReload: Skip automatic window reload (requires manual reload)

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$BumpType = 'patch',
    
    [switch]$NoReload = $false
)

$ErrorActionPreference = 'Stop'

# Navigate to extension directory using relative paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$extDir = $scriptDir  # Script is in ext/ directory
Set-Location $extDir

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Trace Notebook Version Bump" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Read current version from package.json
$packageJsonPath = Join-Path $extDir "package.json"
if (-not (Test-Path $packageJsonPath)) {
    Write-Host "ERROR: package.json not found at $packageJsonPath" -ForegroundColor Red
    exit 1
}
$packageJson = Get-Content $packageJsonPath -Raw | ConvertFrom-Json
$currentVersion = $packageJson.version
Write-Host "Current version: $currentVersion" -ForegroundColor Yellow

# Parse version
$versionParts = $currentVersion -split '\.'
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]
$patch = [int]$versionParts[2]

# Bump version based on type
switch ($BumpType) {
    'major' { 
        $major++
        $minor = 0
        $patch = 0
    }
    'minor' { 
        $minor++
        $patch = 0
    }
    'patch' { 
        $patch++
    }
}

$newVersion = "$major.$minor.$patch"
Write-Host "New version:     $newVersion" -ForegroundColor Green
Write-Host ""

# Update package.json
Write-Host "[1/5] Updating package.json..." -ForegroundColor Cyan
$packageJsonContent = Get-Content $packageJsonPath -Raw
$packageJsonContent = $packageJsonContent -replace "`"version`":\s*`"$currentVersion`"", "`"version`": `"$newVersion`""
# Write without BOM to avoid vsce JSON parse errors
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($packageJsonPath, $packageJsonContent, $utf8NoBom)
# Give filesystem time to sync
Start-Sleep -Milliseconds 200
Write-Host "      Done: package.json updated" -ForegroundColor Green

# Package extension
Write-Host "[2/5] Packaging extension..." -ForegroundColor Cyan
# Remove old vsix files first
Remove-Item "$extDir\trace-notebook-*.vsix" -Force -ErrorAction SilentlyContinue
# Kill Cursor's sandbox offline mode entirely
Remove-Item Env:\npm_config_offline -ErrorAction SilentlyContinue
Remove-Item Env:\npm_config_prefer_offline -ErrorAction SilentlyContinue
$env:npm_config_offline = $null
$env:npm_config_prefer_offline = $null

# Check for local vsce, else try global/npx
$vsceExe = Join-Path $extDir "node_modules\.bin\vsce.cmd"
$ErrorActionPreference = 'Continue'  # Don't fail on stderr
if (Test-Path $vsceExe) {
    $output = & $vsceExe package --allow-missing-repository --allow-star-activation 2>&1
} else {
    # Try npx - redirect stderr to stdout to avoid PowerShell treating warnings as errors
    $output = & npx @vscode/vsce package --allow-missing-repository --allow-star-activation 2>&1
}
$packExitCode = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($packExitCode -ne 0) {
    Write-Host "      ERROR: Packaging failed!" -ForegroundColor Red
    Write-Host $output -ForegroundColor Red
    exit 1
}
# Verify the file was created
Start-Sleep -Milliseconds 500
$vsixPath = Join-Path $extDir "trace-notebook-$newVersion.vsix"
if (-not (Test-Path $vsixPath)) {
    Write-Host "      ERROR: VSIX file not created: $vsixPath" -ForegroundColor Red
    exit 1
}
Write-Host "      Done: Extension packaged: trace-notebook-$newVersion.vsix" -ForegroundColor Green

# Uninstall old extension
Write-Host "[3/5] Uninstalling old extension..." -ForegroundColor Cyan
cursor --uninstall-extension agilebot.trace-notebook 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      Note: Extension may not have been installed" -ForegroundColor Yellow
} else {
    Write-Host "      Done: Old extension uninstalled" -ForegroundColor Green
}

# Install new extension
Write-Host "[4/5] Installing new extension..." -ForegroundColor Cyan
cursor --install-extension "$vsixPath" --force 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Installation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "      Done: Extension v$newVersion installed" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Extension upgraded: $currentVersion -> $newVersion" -ForegroundColor Green
Write-Host ""

# Auto-reload window by default
if (-not $NoReload) {
    Write-Host "[5/5] Reloading Cursor window..." -ForegroundColor Cyan
    try {
        $reloadCmd = "cursor://command/workbench.action.reloadWindow"
        Start-Process $reloadCmd -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
        Write-Host "      Done: Window reload triggered" -ForegroundColor Green
        Write-Host ""
        Write-Host "Extension v$newVersion will be active momentarily!" -ForegroundColor Green
    } catch {
        Write-Host "      Warning: Could not auto-reload. Please reload manually:" -ForegroundColor Yellow
        Write-Host "      Press Ctrl+Shift+P -> Developer: Reload Window" -ForegroundColor Yellow
    }
} else {
    Write-Host "Extension installed successfully!" -ForegroundColor Green
    Write-Host "Reload when ready: Ctrl+Shift+P -> Developer: Reload Window" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "To open a trace notebook:" -ForegroundColor Cyan
Write-Host "  1. Create a .trace file or run 'Trace: Open Trace Notebook' command" -ForegroundColor Yellow
Write-Host "  2. Use 'Trace: Expand Cell' to drill into code references" -ForegroundColor Yellow
Write-Host ""
