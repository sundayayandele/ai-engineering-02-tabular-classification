provider "aws" {
  region = var.aws_region
}
resource "aws_ecr_repository" "churn" {
  name                 = var.repository_name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
output "repository_url" {
  value = aws_ecr_repository.churn.repository_url
}
