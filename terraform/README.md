# Movie REST API – Terraform ECS/Fargate Deployment

This Terraform stack provisions:

- VPC with public/private subnets, IGW, NAT, routes
- Security groups for ALB and ECS service
- Application Load Balancer (HTTP/80) with health checks
- ECR repository for container images
- CloudWatch log group for task logs
- IAM roles (task execution + task role)
- ECS cluster, task definition, and Fargate service

## Structure (Vendor-style)

- modules/: reusable infrastructure modules (network, alb, ecr, logs, iam, ecs_service)
- environments/: per-environment stacks wiring modules together (dev, prod, etc.)

Use environments/dev as your working directory.

## Prerequisites

- AWS account and credentials configured (e.g., via `aws configure`)
- Terraform 1.4+ (>= 1.4.0, < 2.0.0)
- Docker to build the image

## Variables

Key variables (see `variables.tf`):

- `aws_region`: AWS region (default `us-west-2`)
- `project_name`: Resource name prefix
- `image_tag`: Docker image tag to deploy (must exist in ECR)
- `database_url`, `jwt_secret`, `environment`: App runtime configuration

## Deploy Steps

1. Initialize Terraform (environment-based):

```powershell
cd terraform/environments/dev
terraform init
```

2. Create ECR repo (part of apply), then build and push the Docker image:

```powershell
# Get ECR login
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$REGION = "us-west-2" # adjust or set to your var
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build image
$REPO_URL = (terraform output -raw ecr_repository_url)
docker build -t $REPO_URL:latest ..

# Push image
docker push $REPO_URL:latest
```

3. Apply infrastructure:

```powershell
terraform apply -auto-approve
```

4. Access the API via the ALB DNS:

```powershell
terraform output alb_dns_name
```

Open `http://<alb_dns_name>/health` to verify.

## Updating the Service

- Push a new tag (e.g., `v1`), then update `-var image_tag=v1` on apply:

```powershell
# Build and push tag v1
$REPO_URL = (terraform output -raw ecr_repository_url)
docker build -t $REPO_URL:v1 ..
docker push $REPO_URL:v1

# Update service to v1
terraform apply -var "image_tag=v1" -auto-approve
```

## Notes

- Fargate service runs in private subnets behind the public ALB.
- Health check path is `/health` and container listens on port `8000`.
- `auto_create_schema` is disabled for production tasks.
