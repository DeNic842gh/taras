# Run API + marine site locally (when Docker is broken)
Set-Location $PSScriptRoot\..

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Write-Host "Starting FastAPI on http://localhost:8000" -ForegroundColor Green
Write-Host "Marine site: http://localhost:8000/marine/" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

$env:USE_MEMORY_STORE = "true"
$env:HOST = "0.0.0.0"
$env:PORT = "8000"
poetry run python main.py
