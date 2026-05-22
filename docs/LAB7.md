# Lab 7 — Prometheus & Grafana monitoring

## Stack (Docker)

| Service | Container | Port | Role |
|---------|-----------|------|------|
| Prometheus | `fastapi_prometheus` | 9090 | Metrics storage & scraping |
| Grafana | `fastapi_grafana` | 3000 | Dashboards (admin / admin) |
| docker-stats-exporter | `fastapi_docker_exporter` | 9417 | **[docker]** container metrics (Docker API; works on Windows) |
| postgres_exporter | `fastapi_postgres_exporter` | 9187 | **[postgresql]** DB metrics |
| FastAPI | `fastapi_app` | 8000 | **[fastAPI]** `/metrics` + custom counters |

## Start

**Important:** `docker compose up` alone only starts **API + PostgreSQL**. Grafana is in a second compose file — you must merge both:

```powershell
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build
```

Or:

```powershell
.\scripts\start-monitoring.ps1
```

If http://localhost:3000 shows **Error -102** (connection refused), Grafana is not running — run the command above.

### Two compose projects in Docker Desktopa

| Project | Containers | Purpose |
|---------|--------------|---------|
| **fastapi** | `fastapi_app`, `fastapi_postgres`, + monitoring when started | Main app (Lab 2–7) |
| **fastapi-test** | `fastapi_postgres_test` | Lab 6 tests only (port 5433) |

They are **separate on purpose** — not a connection error between them.

Wait ~30s, then open:

- Grafana: http://localhost:3000 (login `admin` / `admin`)
- Prometheus: http://localhost:9090
- API metrics: http://localhost:8000/metrics

## Dashboards (folder **Lab 7 Monitoring**)

All panel titles use the required prefixes:

| Dashboard | Prefix | Panels |
|-----------|--------|--------|
| `[fastAPI] Application Overview` | `[fastAPI]` | Request rate, latency p95, status codes, in-progress |
| `[postgresql] Database Overview` | `[postgresql]` | Up, connections, DB size, TPS, cache hits |
| `[docker] Containers Overview` | `[docker]` | CPU, memory, network RX/TX per container |
| `[custom] Marine Site & App Metrics` | `[custom]` / `[fastAPI]` | Treasure clicks, gallery clicks, registrations |

Prometheus scrape jobs are also named `[fastAPI] api`, `[postgresql] exporter`, `[docker] cadvisor`.

## Custom metrics

| Metric | Trigger |
|--------|---------|
| `fastapi_marine_treasure_clicks_total` | Treasure chest button on `/marine/` |
| `fastapi_marine_gallery_clicks_total` | Gallery thumbnail click |
| `fastapi_auth_registrations_total` | Successful `POST /api/v1/auth/register` |

Generate traffic for screenshots:

```powershell
# API traffic
1..20 | ForEach-Object { Invoke-WebRequest -Uri http://127.0.0.1:8000/api/v1/health -UseBasicParsing | Out-Null }

# Marine site + custom metrics (open in browser)
# http://127.0.0.1:8000/marine/ — click treasure chest & gallery thumbs
```

## Screenshots for **dev** branch

Save PNG files under `photo/Lab7/`:

1. `prometheus-targets.png` — Status → Targets, all 3 jobs UP
2. `grafana-fastapi.png` — `[fastAPI] Application Overview` dashboard
3. `grafana-postgresql.png` — `[postgresql] Database Overview`
4. `grafana-docker.png` — `[docker] Containers Overview`
5. `grafana-custom.png` — `[custom] Marine Site & App Metrics` with clicks > 0
6. `prometheus-custom-metric.png` — Prometheus graph of `fastapi_marine_treasure_clicks_total`

```powershell
git checkout dev
git add monitoring/ docker-compose.monitoring.yml photo/Lab7/ docs/LAB7.md
git commit -m "Lab 7: Prometheus, Grafana, custom metrics, dashboards"
```

## Troubleshooting

### Prometheus: `error mounting` / `failed to create shim task`

**Cause:** `monitoring/prometheus/prometheus.yml` exists as a **folder** instead of a **file** (Docker cannot bind-mount a directory onto a file path).

**Fix:**

```powershell
Remove-Item -Recurse -Force monitoring\prometheus\prometheus.yml
# File monitoring/prometheus/prometheus.yml must exist (see repo)
.\scripts\docker-fix-and-start.ps1
```

The compose file mounts the whole `./monitoring/prometheus` directory to `/etc/prometheus` to avoid single-file mount issues on Windows.

### `python: can't open file '/app/main.py'`

The API image must include root `main.py`. Rebuild:

```powershell
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml build --no-cache api
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d api
```

Or run `.\scripts\docker-fix-and-start.ps1`.

### cAdvisor: `failed to identify the read-write layer ID` / `mount-id: no such file`

Docker’s internal layer database is corrupted (often after disk I/O errors). Steps:

1. **Docker Desktop → Troubleshoot → Clean / Purge data** (or Reset to factory defaults)
2. Reboot PC
3. `.\scripts\docker-fix-and-start.ps1`

These cAdvisor warnings are **noise from ghost containers**; they stop after a clean Docker reset and `docker compose down --remove-orphans`.

### `input/output error` on `meta.db`

Docker Desktop cannot write its database — restart Docker, free disk space on `C:`, or reinstall Docker Desktop.

### Prometheus / Grafana restart loop (exit code 135)

On some **Windows + Docker Desktop** setups, `prom/prometheus:v2.54.x` and `grafana/grafana:11.x` crash immediately (exit **135**). This project uses stable versions instead:

- `prom/prometheus:v2.47.2`
- `grafana/grafana:10.4.3`

```powershell
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml down --remove-orphans
docker volume rm fastapi_prometheus_data fastapi_grafana_data
.\scripts\docker-fix-and-start.ps1
```

### [docker] Grafana shows "No data" on Windows

**cAdvisor does not work** on Docker Desktop for Windows (overlayfs / `mount-id` errors). This project uses **`docker-stats-exporter`** instead (Docker API via socket).

```powershell
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d --build docker_stats_exporter prometheus grafana
docker restart fastapi_prometheus fastapi_grafana
docker rm -f fastapi_cadvisor 2>$null   # optional: remove old cAdvisor
```

Check metrics exist:

```powershell
curl http://127.0.0.1:9417/metrics | findstr docker_container_cpu
```

In Prometheus query: `docker_container_cpu_usage_percent{job="docker_stats_exporter"}`

Grafana → **[docker] Containers Overview** → time range **Last 15 minutes** → refresh **10s**.

## Verify targets

Prometheus → **Status → Targets** should show:

- `[fastAPI] api` — UP
- `[postgresql] exporter` — UP
- `[docker] cadvisor` — UP
