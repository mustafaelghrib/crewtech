variable "aws" {
  type    = map(string)
  default = {
    region     = ""
    access_key = ""
    secret_key = ""
    account_id = ""
  }
}

provider "aws" {
  region     = var.aws.region
  access_key = var.aws.access_key
  secret_key = var.aws.secret_key
}

variable "database_password" { type = string }

module "aws" {
  source = "./modules/aws"

  bucket_access_key = var.aws.access_key
  bucket_secret_key = var.aws.secret_key
  bucket_name       = "${local.project_name}-bucket"
  bucket_acl        = "private"

  database_identifier        = "${local.project_name}-database"
  database_name              = "${local.project_name}_db"
  database_username          = "${local.project_name}_user"
  database_password          = var.database_password
  database_port              = 5432
  database_engine            = "postgres"
  database_engine_version    = "13.7"
  database_instance_class    = "db.t3.micro"
  database_storage_type      = "gp2"
  database_allocated_storage = "20"

  instance_name            = "${local.project_name}-instance"
  instance_ami             = "ami-08c40ec9ead489470"
  instance_type            = "t2.micro"
  instance_volume_type     = "gp2"
  instance_volume_size     = "20"
  instance_user            = "ubuntu"
  instance_scripts         = ["./scripts/install_docker.sh"]
  instance_ssh_name        = "${local.project_name}-ssh-key"
  instance_ssh_public_key  = file("${path.module}/.ssh/id_rsa.pub")
  instance_ssh_private_key = file("${path.module}/.ssh/id_rsa")

  instance_install_aws_cli_source      = "./scripts/install_aws_cli.sh"
  instance_install_aws_cli_destination = "/tmp/install_aws_cli.sh"
  instance_install_aws_cli_command     = "/tmp/install_aws_cli.sh -C ${var.aws.access_key} -S ${var.aws.secret_key} -R ${var.aws.region} -A ${var.aws.account_id}"

  repository_name = local.project_name
}

output "aws" {
  value     = module.aws
  sensitive = true
}

