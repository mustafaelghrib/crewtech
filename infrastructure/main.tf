terraform {
  required_version = "1.3.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    circleci = {
      source  = "mrolla/circleci"
      version = "0.6.1"
    }
  }
  backend "s3" {}
}

locals { project_name = "crewtech" }
