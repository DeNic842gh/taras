# Lab 7 — start API + DB + Prometheus + Grafana
Set-Location $PSScriptRoot\..

Write-Host "Starting fastapi + monitoring stack..." -ForegroundColor Cyan
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build

Write-Host ""
Write-Host "When all containers are Up:" -ForegroundColor Green
Write-Host "  Grafana:    http://localhost:3000  (admin / admin)"
Write-Host "  Prometheus: http://localhost:9090"
Write-Host "  API:        http://localhost:8000"
Write-Host ""
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml ps
