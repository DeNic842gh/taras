# Fix CRLF in entrypoint, rebuild API image, start stack.
# If Docker returns 500 / I/O errors: restart Docker Desktop, then run this again.
Set-Location $PSScriptRoot\..

$entrypoint = Join-Path $PSScriptRoot "docker-entrypoint.sh"
if (Test-Path $entrypoint) {
    $text = [System.IO.File]::ReadAllText($entrypoint) -replace "`r`n", "`n" -replace "`r", "`n"
    [System.IO.File]::WriteAllText($entrypoint, $text, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Normalized docker-entrypoint.sh to LF." -ForegroundColor Cyan
}

Write-Host "Stopping old containers..." -ForegroundColor Yellow
docker compose down 2>$null

Write-Host "Building api (no cache)..." -ForegroundColor Yellow
docker compose build --no-cache api
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Restart Docker Desktop, then run this script again." -ForegroundColor Red
    Write-Host "Local fallback: .\scripts\start-local.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting db + api..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Start failed. Check Docker Desktop is running." -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 5
docker compose ps
Write-Host ""
Write-Host "Marine site: http://localhost:8000/marine/" -ForegroundColor Green
Write-Host "API health:  http://localhost:8000/api/v1/health" -ForegroundColor Green
