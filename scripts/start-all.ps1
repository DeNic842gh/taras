# Start full project: API + DB + monitoring (+ optional test DB)
Set-Location $PSScriptRoot\..

Write-Host "=== FastAPI main stack + monitoring ===" -ForegroundColor Cyan
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build

Write-Host ""
Write-Host "=== Test DB (Lab 6, port 5433) ===" -ForegroundColor Cyan
docker compose -f docker-compose.test.yml up -d

Write-Host ""
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml ps
Write-Host ""
Write-Host "URLs:" -ForegroundColor Green
Write-Host "  API:        http://localhost:8000"
Write-Host "  Docs:       http://localhost:8000/docs"
Write-Host "  Marine:     http://localhost:8000/marine/"
Write-Host "  Grafana:    http://localhost:3000  (admin / admin)"
Write-Host "  Prometheus: http://localhost:9090"
Write-Host ""
Write-Host "Docker Desktop: look for project 'fastapi' (not only fastapi-test)" -ForegroundColor Yellow
