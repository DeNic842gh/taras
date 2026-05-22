# Lab 8 — manual deploy helper (requires AWS CLI + Terraform + Docker)
param(
    [string]$Region = $env:AWS_REGION,
    [string]$ImageTag = "manual-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$TfDir = Join-Path $Root "infra\terraform"

if (-not $Region) {
    $Region = Read-Host "AWS_REGION (e.g. eu-central-1)"
}

Write-Host "==> Terraform apply (image_tag=$ImageTag)" -ForegroundColor Cyan
Push-Location $TfDir
terraform init -input=false
$env:TF_VAR_aws_region = $Region
$env:TF_VAR_image_tag = $ImageTag
terraform apply -auto-approve -input=false

$EcrRepo = terraform output -raw ecr_repository_name
$EcrUrl = terraform output -raw ecr_repository_url
$Cluster = terraform output -raw ecs_cluster_name
$Service = terraform output -raw ecs_service_name
$AppUrl = terraform output -raw application_url
Pop-Location

Write-Host "==> Docker build & push to $EcrUrl" -ForegroundColor Cyan
$Account = (aws sts get-caller-identity --query Account --output text)
$Registry = "$Account.dkr.ecr.$Region.amazonaws.com"
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $Registry

Push-Location $Root
$ImageUri = "${Registry}/${EcrRepo}:${ImageTag}"
docker build -t $ImageUri .
docker push $ImageUri
Pop-Location

Write-Host "==> ECS force new deployment" -ForegroundColor Cyan
aws ecs update-service --cluster $Cluster --service $Service --force-new-deployment --region $Region
aws ecs wait services-stable --cluster $Cluster --services $Service --region $Region

Write-Host ""
Write-Host "Deployed: $AppUrl" -ForegroundColor Green
Write-Host "Docs:     $AppUrl/docs"
Write-Host "Marine:   $AppUrl/marine/"
