terraform {
  required_providers {
    circleci = {
      source  = "mrolla/circleci"
    }
  }
}

variable "context_name" { type = string }
variable "context_env" { type = map(any) }

resource "circleci_context" "main" {
  name = var.context_name
}

resource "circleci_context_environment_variable" "main" {
  for_each   = var.context_env
  variable   = each.key
  value      = each.value
  context_id = circleci_context.main.id
}
