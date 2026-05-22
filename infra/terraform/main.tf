data "aws_caller_identity" "current" {}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "random_password" "db" {
  count   = var.db_password == "" ? 1 : 0
  length  = 24
  special = false
}

resource "random_password" "app_secret" {
  count   = var.secret_key == "" ? 1 : 0
  length  = 48
  special = true
}

locals {
  name_prefix  = var.project_name
  db_username  = "app"
  db_name      = "fastapi_db"
  db_password  = var.db_password != "" ? var.db_password : random_password.db[0].result
  secret_key   = var.secret_key != "" ? var.secret_key : random_password.app_secret[0].result
  image_uri    = "${aws_ecr_repository.api.repository_url}:${var.image_tag}"
  database_url = "postgresql+asyncpg://${local.db_username}:${local.db_password}@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${local.db_name}"
}
