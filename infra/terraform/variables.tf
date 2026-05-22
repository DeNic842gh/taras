variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Prefix for resource names (ECR, ECS, RDS, etc.)"
  type        = string
  default     = "fastapi"
}

variable "image_tag" {
  description = "Docker image tag deployed to ECS (set by CI/CD, e.g. git SHA)"
  type        = string
  default     = "latest"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "fargate_cpu" {
  description = "Fargate task CPU units (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "fargate_memory" {
  description = "Fargate task memory in MiB"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Number of ECS tasks behind the load balancer"
  type        = number
  default     = 1
}

variable "db_password" {
  description = "RDS master password (leave empty to auto-generate)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "secret_key" {
  description = "FastAPI SECRET_KEY for JWT (leave empty to auto-generate)"
  type        = string
  sensitive   = true
  default     = ""
}
