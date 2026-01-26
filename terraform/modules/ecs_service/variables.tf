variable "project_name" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "ecs_service_security_group_id" { type = string }
variable "target_group_arn" { type = string }
variable "log_group_name" { type = string }
variable "aws_region" { type = string }
variable "ecr_repository_url" { type = string }
variable "image_tag" { type = string }
variable "container_port" { type = number }
variable "desired_count" { type = number }
variable "task_cpu" { type = number }
variable "task_memory" { type = number }
variable "task_execution_role_arn" { type = string }
variable "task_role_arn" { type = string }
variable "database_url" { type = string }
variable "jwt_secret" {
	type      = string
	sensitive = true
}
variable "environment" { type = string }
