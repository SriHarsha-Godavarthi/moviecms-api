module "network" {
  source                = "../../modules/network"
  project_name          = var.project_name
  vpc_cidr              = var.vpc_cidr
  public_subnet_cidrs   = var.public_subnet_cidrs
  private_subnet_cidrs  = var.private_subnet_cidrs
  container_port        = var.container_port
}

module "alb" {
  source                 = "../../modules/alb"
  project_name           = var.project_name
  vpc_id                 = module.network.vpc_id
  public_subnet_ids      = module.network.public_subnet_ids
  alb_security_group_id  = module.network.alb_security_group_id
  container_port         = var.container_port
  health_check_path      = var.health_check_path
}

module "ecr" {
  source       = "../../modules/ecr"
  project_name = var.project_name
}

module "logs" {
  source       = "../../modules/logs"
  project_name = var.project_name
}

module "iam" {
  source       = "../../modules/iam"
  project_name = var.project_name
}

module "ecs_service" {
  source                         = "../../modules/ecs_service"
  project_name                   = var.project_name
  private_subnet_ids             = module.network.private_subnet_ids
  ecs_service_security_group_id  = module.network.ecs_service_security_group_id
  target_group_arn               = module.alb.target_group_arn
  log_group_name                 = module.logs.log_group_name
  aws_region                     = var.aws_region
  ecr_repository_url             = module.ecr.repository_url
  image_tag                      = var.image_tag
  container_port                 = var.container_port
  desired_count                  = var.desired_count
  task_cpu                       = var.task_cpu
  task_memory                    = var.task_memory
  task_execution_role_arn        = module.iam.task_execution_role_arn
  task_role_arn                  = module.iam.task_role_arn
  database_url                   = var.database_url
  jwt_secret                     = var.jwt_secret
  environment                    = var.environment
}

output "alb_dns_name" {
  value = module.alb.alb_dns_name
}
output "ecr_repository_url" {
  value = module.ecr.repository_url
}
output "ecs_cluster_name" {
  value = module.ecs_service.cluster_name
}
output "ecs_service_name" {
  value = module.ecs_service.service_name
}
