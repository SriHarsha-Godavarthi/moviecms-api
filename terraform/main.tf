// Intentionally left minimal. See dedicated files:
// - provider.tf: AWS provider & versions
// - variables.tf: deployment variables
// - vpc.tf: VPC, subnets, IGW/NAT, routes, SGs
// - alb.tf: Application Load Balancer & target group
// - ecr.tf: ECR repository
// - logs.tf: CloudWatch log group
// - iam.tf: ECS task roles and policies
// - ecs.tf: Cluster, task definition, and Fargate service
// - outputs.tf: useful outputs (ALB DNS, ECR URL)

// Keeping this file as an index for Terraform module layout.
