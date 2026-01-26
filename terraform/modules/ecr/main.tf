resource "aws_ecr_repository" "repo" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"

  encryption_configuration { encryption_type = "AES256" }
  tags = { Name = var.project_name }
}
