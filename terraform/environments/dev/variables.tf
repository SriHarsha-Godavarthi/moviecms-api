variable "aws_region" {
	type    = string
	default = "us-west-2"
}

variable "project_name" {
	type    = string
	default = "movie-restapi"
}

variable "vpc_cidr" {
	type    = string
	default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
	type    = list(string)
	default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
	type    = list(string)
	default = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "container_port" {
	type    = number
	default = 8000
}

variable "desired_count" {
	type    = number
	default = 2
}

variable "health_check_path" {
	type    = string
	default = "/health"
}

variable "image_tag" {
	type    = string
	default = "latest"
}

variable "task_cpu" {
	type    = number
	default = 512
}

variable "task_memory" {
	type    = number
	default = 1024
}

variable "database_url" {
	type    = string
	default = "sqlite+aiosqlite:///./movieflix.db"
}

variable "jwt_secret" {
	type      = string
	default   = "change_me_in_production"
	sensitive = true
}

variable "environment" {
	type    = string
	default = "production"
}
