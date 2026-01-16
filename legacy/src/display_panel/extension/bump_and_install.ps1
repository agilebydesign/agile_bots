# Bump version, rebuild, and reinstall the REPL Status Panel extension
# Usage: .\bump_and_install.ps1 [patch|minor|major]
# Default: patch (0.24.7 -> 0.24.8)

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$BumpType = 'patch'
)

$ErrorActionPreference = 'Stop'

# Navigate to extension directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "================================" -ForegroundColor Cyan
Write-Host "REPL Status Panel Version Bump" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Read current version from package.json
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
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
Write-Host "[1/6] Updating package.json..." -ForegroundColor Cyan
$packageJsonContent = Get-Content "package.json" -Raw
$packageJsonContent = $packageJsonContent -replace "`"version`": `"$currentVersion`"", "`"version`": `"$newVersion`""
Set-Content "package.json" -Value $packageJsonContent -NoNewline
Write-Host "      Done: package.json updated" -ForegroundColor Green

# Update html_renderer.js
Write-Host "[2/6] Updating html_renderer.js..." -ForegroundColor Cyan
$htmlRendererContent = Get-Content "html_renderer.js" -Raw
$htmlRendererContent = $htmlRendererContent -replace "v$currentVersion", "v$newVersion"
Set-Content "html_renderer.js" -Value $htmlRendererContent -NoNewline
Write-Host "      Done: html_renderer.js updated" -ForegroundColor Green

# Package extension
Write-Host "[3/6] Packaging extension..." -ForegroundColor Cyan
npx @vscode/vsce package --allow-missing-repository --allow-star-activation | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Packaging failed!" -ForegroundColor Red
    exit 1
}
Write-Host "      Done: Extension packaged: repl-status-panel-$newVersion.vsix" -ForegroundColor Green

# Uninstall old extension
Write-Host "[4/6] Uninstalling old extension..." -ForegroundColor Cyan
cursor --uninstall-extension agilebot.repl-status-panel | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "      Warning: Uninstall warning (may not be installed)" -ForegroundColor Yellow
} else {
    Write-Host "      Done: Old extension uninstalled" -ForegroundColor Green
}

# Install new extension
Write-Host "[5/6] Installing new extension..." -ForegroundColor Cyan
$vsixPath = Join-Path $scriptDir "repl-status-panel-$newVersion.vsix"
cursor --install-extension "$vsixPath" | Out-Null
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
Write-Host "[6/6] Reloading Cursor window..." -ForegroundColor Cyan

# Give extension time to register
Start-Sleep -Seconds 1

# Automate keyboard input to trigger reload
try {
    Add-Type -AssemblyName System.Windows.Forms
    
    # Find and focus Cursor window
    $cursorProcess = Get-Process | Where-Object { $_.ProcessName -eq "Cursor" -and $_.MainWindowTitle -ne "" } | Select-Object -First 1
    
    if ($cursorProcess) {
        # Focus the Cursor window
        $sig = '[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);'
        $type = Add-Type -MemberDefinition $sig -Name WindowAPI -PassThru
        $null = $type::SetForegroundWindow($cursorProcess.MainWindowHandle)
        
        Start-Sleep -Milliseconds 500
        
        # Send Ctrl+Shift+P to open command palette
        [System.Windows.Forms.SendKeys]::SendWait("^+p")
        
        Start-Sleep -Milliseconds 800
        
        # Type the reload command
        [System.Windows.Forms.SendKeys]::SendWait("Developer: Reload Window")
        
        Start-Sleep -Milliseconds 500
        
        # Press Enter
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "      Done: Cursor window reload triggered!" -ForegroundColor Green
    } else {
        Write-Host "      Warning: Could not find Cursor window. Please reload manually." -ForegroundColor Yellow
    }
} catch {
    Write-Host "      Warning: Automation failed. Please reload manually (Ctrl+Shift+P -> Developer: Reload Window)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Extension v$newVersion will be active after reload!" -ForegroundColor Green
Write-Host ""
