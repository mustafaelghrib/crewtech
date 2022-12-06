variable "aws" {
  type    = map(string)
  default = {
    region     = ""
    access_key = ""
    secret_key = ""
  }
}

provider "aws" {
  region     = var.aws.region
  access_key = var.aws.access_key
  secret_key = var.aws.secret_key
}

module "aws" {
  source = "./modules/aws"

  bucket_access_key = var.aws.access_key
  bucket_secret_key = var.aws.secret_key
  bucket_name       = "${local.project_name}-bucket"
  bucket_acl        = "private"

}

output "aws" {
  value     = module.aws
  sensitive = true
}

