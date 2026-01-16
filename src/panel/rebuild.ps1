# Rebuild and reinstall Bot Panel extension
# Usage: .\rebuild.ps1

# Increment patch version in package.json
Write-Host "Incrementing version number..." -ForegroundColor Cyan
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
$version = [version]$packageJson.version
$newVersion = "{0}.{1}.{2}" -f $version.Major, $version.Minor, ($version.Build + 1)
$packageJson.version = $newVersion
$jsonContent = $packageJson | ConvertTo-Json -Depth 100
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText("$PWD\package.json", $jsonContent, $utf8NoBom)
Write-Host "Version updated: $($version) -> $newVersion" -ForegroundColor Green

Write-Host "Cleaning up old VSIX files..." -ForegroundColor Cyan
Remove-Item *.vsix -ErrorAction SilentlyContinue

Write-Host "Packaging extension..." -ForegroundColor Cyan
npx @vscode/vsce package --allow-missing-repository

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Packaging failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Finding latest VSIX..." -ForegroundColor Cyan
$vsix = Get-ChildItem -Filter *.vsix | Select-Object -First 1

if ($vsix) {
    Write-Host "Uninstalling old extensions (if exist)..." -ForegroundColor Cyan
    cursor --uninstall-extension agilebot.bot-panel 2>$null
    cursor --uninstall-extension agilebot.repl-status-panel 2>$null
    
    Write-Host "Installing $($vsix.Name)..." -ForegroundColor Cyan
    cursor --install-extension $vsix.FullName --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nExtension rebuilt and installed!" -ForegroundColor Green
        Write-Host "Reloading Cursor window..." -ForegroundColor Yellow
        
        # Reload the window using VS Code command
        cursor --reuse-window --command "workbench.action.reloadWindow"
        
        Write-Host "Window reload command sent!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Installation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: No VSIX file found" -ForegroundColor Red
    exit 1
}
