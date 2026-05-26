# Lab 8 — AWS deployment & GitHub Actions CI/CD

Deploy the FastAPI app to **AWS** (ECS Fargate + RDS PostgreSQL + ALB + ECR) and automate **build → test → deploy** with **GitHub Actions**.

## Architecture

```mermaid
flowchart LR
  subgraph GitHub
    PR[Pull request] --> CI[CI workflow]
    Main[Push main/prod] --> CD[Deploy workflow]
  end
  subgraph AWS
    ECR[ECR fastapi-api]
    ECS[ECS Fargate]
    RDS[(RDS PostgreSQL)]
    ALB[Application Load Balancer]
  end
  CI -->|pytest + ruff + docker build| CI
  CD -->|terraform apply| ECR
  CD -->|docker push| ECR
  CD -->|ecs update-service| ECS
  ALB --> ECS
  ECS --> RDS
  User[Browser] --> ALB
```

| Component | AWS service | Purpose |
|-----------|-------------|---------|
| API container | **ECS Fargate** | Runs Docker image (port 8000) |
| Database | **RDS PostgreSQL 16** | Production `fastapi_db` (private) |
| Images | **ECR** | Stores `fastapi-api` images |
| Public URL | **ALB** | `http://<alb-dns>/docs`, `/marine/` |
| Logs | **CloudWatch** | `/ecs/fastapi-api` |

Terraform lives in [`infra/terraform/`](../infra/terraform/).

## Prerequisites

1. **AWS account** (Free Tier eligible: `db.t3.micro`, 1 Fargate task).
2. **IAM user** for CI/CD with permissions for ECR, ECS, RDS, EC2 (VPC/SG), ELB, IAM (roles), CloudWatch Logs, Terraform state (if using S3 backend).
3. **Terraform** ≥ 1.5 locally (optional; CD runs it in GitHub).
4. **GitHub repository** with this code pushed.
ssh -i aws-key.pem ubuntu@16.171.168.211
## 1. Configure GitHub Secrets

Repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret | Required | Example |
|--------|----------|---------|
| `AWS_ACCESS_KEY_ID` | Yes | IAM access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | IAM secret key |
| `AWS_REGION` | Yes | `eu-central-1` |
| `TF_VAR_db_password` | No | Strong DB password (omit → auto-generated, stored in Terraform state) |
| `TF_VAR_secret_key` | No | Long JWT `SECRET_KEY` (omit → auto-generated) |

See [`.env.aws.example`](../.env.aws.example) for a checklist.

## 2. Workflows

| File | Trigger | What it does |
|------|---------|----------------|
| [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Push/PR to `main`, `dev`, `prod` | Ruff, pytest (PostgreSQL service), Docker build |
| [`.github/workflows/deploy-aws.yml`](../.github/workflows/deploy-aws.yml) | Push to `main` or `prod`, or manual | Terraform apply → ECR push → ECS rolling deploy |
| [`.github/workflows/terraform-plan.yml`](../.github/workflows/terraform-plan.yml) | PR changing `infra/terraform/` | Posts Terraform plan comment |

### CI (local equivalent)

```powershell
docker compose -f docker-compose.test.yml up -d
$env:TEST_DATABASE_URL = "postgresql+asyncpg://app:appsecret@127.0.0.1:5433/fastapi_test_db"
poetry run ruff check app tests
poetry run pytest
docker build -t fastapi-api:local .
```

### First AWS deploy (manual, optional)

```powershell
cd infra/terraform
copy terraform.tfvars.example terraform.tfvars
# Edit aws_region if needed
terraform init
terraform apply -var="image_tag=bootstrap"
```

Then configure GitHub secrets and push to `main` — **Deploy to AWS** workflow builds the real image and updates ECS.

## 3. Verify deployment

After a successful **Deploy to AWS** run:

1. Open the workflow **Summary** — it prints the ALB URL.
2. Or run locally:
   ```powershell
   cd infra/terraform
   terraform output application_url
   ```
3. Check endpoints:
   - Health: `http://<alb>/api/v1/health`
   - Swagger: `http://<alb>/docs`
   - Marine site: `http://<alb>/marine/`

ECS tasks run **Alembic migrations** on startup (`scripts/docker-entrypoint.sh`).

### Logs

```powershell
aws logs tail /ecs/fastapi-api --follow --region eu-central-1
```

## 4. Docker image (production)

[`Dockerfile`](../Dockerfile) copies `main.py`, runs migrations, then starts the API.

Rebuild locally:

```powershell
docker compose up -d --build
```

## 5. Cost & cleanup

- **RDS** `db.t3.micro` and **Fargate** incur cost after Free Tier limits.
- Destroy everything when finished:

```powershell
cd infra/terraform
terraform destroy
```

Also delete orphaned **ECR** images if the repository was removed manually.

## 6. Screenshots for `dev` branch (`photo/Lab8/`)

| File | Content |
|------|---------|
| `github-ci-success.png` | Actions → CI workflow green |
| `github-deploy-success.png` | Actions → Deploy to AWS green |
| `terraform-apply.png` | Local or CI Terraform apply output |
| `ecs-service-running.png` | ECS console — service stable, 1/1 tasks |
| `alb-health.png` | Target group healthy |
| `aws-api-docs.png` | Browser `/docs` on ALB URL |
| `aws-marine-site.png` | Browser `/marine/` on ALB URL |

## 7. Troubleshooting

| Problem | Fix |
|---------|-----|
| CI pytest fails | Ensure `TEST_DATABASE_URL` points to Postgres; in GHA the service container uses port **5432** |
| `CannotPullContainerError` | Push image to ECR first; re-run deploy workflow |
| ECS task exits | Check CloudWatch `/ecs/fastapi-api` — often DB not ready or migration error |
| ALB **502** | Wait for health check `/api/v1/health`; check security groups |
| Terraform RDS error | Default VPC must exist in the region; try another region in `terraform.tfvars` |
| Deploy workflow missing secrets | Add all three required AWS secrets |

## 8. Optional: OIDC instead of access keys

For production, prefer **GitHub OIDC** → IAM role (no long-lived keys). Steps:

1. Create IAM OIDC provider for `token.actions.githubusercontent.com`.
2. IAM role with trust policy scoped to your repo.
3. Replace `aws-actions/configure-aws-credentials` with `role-to-assume: arn:aws:iam::...`.

Details: [AWS docs — GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services).

## Related labs

- [LAB6.md](LAB6.md) — pytest (CI uses the same pattern with GHA Postgres)
- [LAB7.md](LAB7.md) — monitoring (optional on AWS; not included in default Terraform stack)
