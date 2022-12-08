variable "circleci" {
  type    = map(string)
  default = {
    api_token    = ""
    vcs_type     = ""
    organization = ""
  }
}

provider "circleci" {
  api_token    = var.circleci.api_token
  vcs_type     = var.circleci.vcs_type
  organization = var.circleci.organization
}

variable "contexts" {
  type    = map(map(string))
  default = {
    common      = {}
    production  = {}
  }
}

module "circleci" {
  for_each     = var.contexts
  source       = "./modules/circleci"
  context_name = "${local.project_name}-${each.key}-context"
  context_env  = each.value
}
