output "aws_region" {
  value = var.aws_region
}

output "ecr_repository_url" {
  description = "Push Docker images here"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_repository_name" {
  value = aws_ecr_repository.api.name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.api.name
}

output "alb_dns_name" {
  description = "Public URL — http://<this>/docs and /marine/"
  value       = aws_lb.api.dns_name
}

output "application_url" {
  value = "http://${aws_lb.api.dns_name}"
}

output "rds_endpoint" {
  description = "RDS hostname (private — reachable from ECS only)"
  value       = aws_db_instance.postgres.address
  sensitive   = true
}

output "database_url" {
  description = "Async SQLAlchemy URL (sensitive)"
  value       = local.database_url
  sensitive   = true
}
