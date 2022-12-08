#AWS Elastic Container Registry

variable "repository_name" { type = string }

resource "aws_ecr_repository" "main" {
  name = var.repository_name
  force_delete = true
}

output "REPOSITORY_URL" { value = aws_ecr_repository.main.repository_url }
