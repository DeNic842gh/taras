resource "aws_db_subnet_group" "postgres" {
  name       = "${local.name_prefix}-db-subnets"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "${local.name_prefix}-postgres"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  storage_type           = "gp3"
  db_name                = local.db_name
  username               = local.db_username
  password               = local.db_password
  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
  backup_retention_period = 0
  deletion_protection    = false
  apply_immediately      = true

  tags = {
    Name = "${local.name_prefix}-postgres"
  }
}
