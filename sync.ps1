#!/usr/bin/env pwsh

# Git Sync Script for Voice Assistant

$projectPath = 'C:\Users\Rishwanth\Desktop\voiceassistant'
Set-Location $projectPath

Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Step 1: Pull from GitHub
Write-Host "📥 Step 1: Pulling from GitHub..." -ForegroundColor Yellow
git pull origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Pull successful" -ForegroundColor Green
} else {
    Write-Host "⚠️  Pull status: $LASTEXITCODE" -ForegroundColor Yellow
}
Write-Host ""

# Step 2: Check status
Write-Host "📊 Step 2: Checking git status..." -ForegroundColor Yellow
$statusOutput = git status --porcelain
if ([string]::IsNullOrEmpty($statusOutput)) {
    Write-Host "✅ Working directory clean - no changes to commit" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Found changes to commit:" -ForegroundColor Cyan
    $statusOutput | Write-Host
}
Write-Host ""

# Step 3: Stage changes
Write-Host "📦 Step 3: Staging changes..." -ForegroundColor Yellow
git add -A
Write-Host "✅ All changes staged" -ForegroundColor Green
Write-Host ""

# Step 4: Commit
Write-Host "💾 Step 4: Creating commit..." -ForegroundColor Yellow
$commitMessage = @"
feat: Add WhatsApp Web fallback and advanced app finder

Backend improvements:
- Add open_whatsapp_web() function for WhatsApp Web fallback
- Improve open_application() with webbrowser support
- Support web:// and ms-settings:// URI schemes
- Better error handling with multi-word app names

New utilities:
- Create app_finder.py with advanced application discovery
- Scan Windows Registry for installed applications
- Comprehensive WhatsApp path detection (7+ locations)
- Windows Start Menu and portable app searching

Features:
- Users now get WhatsApp Web fallback if desktop app unavailable
- Say 'open whatsapp' voice command for automatic browser fallback
- No security concerns - uses safe webbrowser module
"@

git commit -m $commitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit successful" -ForegroundColor Green
} else {
    Write-Host "⚠️  Nothing to commit or error occurred" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Push to GitHub
Write-Host "📤 Step 5: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push successful" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed" -ForegroundColor Red
}
Write-Host ""

# Step 6: Final status
Write-Host "final git status:" -ForegroundColor Cyan
git status
Write-Host ""
Write-Host "✅ Sync complete!" -ForegroundColor Green
