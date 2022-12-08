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
