# Rebuild and reinstall VS Code extension
# Usage: .\rebuild.ps1

Write-Host "Cleaning up old VSIX files..." -ForegroundColor Cyan
Remove-Item *.vsix -ErrorAction SilentlyContinue

Write-Host "Packaging extension..." -ForegroundColor Cyan
npx vsce package

Write-Host "Finding latest VSIX..." -ForegroundColor Cyan
$vsix = Get-ChildItem -Filter *.vsix | Select-Object -First 1

if ($vsix) {
    Write-Host "Installing $($vsix.Name)..." -ForegroundColor Cyan
    code --install-extension $vsix.FullName --force
    
    Write-Host "`nExtension rebuilt and installed!" -ForegroundColor Green
    Write-Host "Reload VS Code window to activate changes (Ctrl+R or Cmd+R)" -ForegroundColor Yellow
} else {
    Write-Host "ERROR: No VSIX file found" -ForegroundColor Red
    exit 1
}
