terraform {
  required_version = "{{ cookiecutter.terraform_required_version }}"

  required_providers {
    aws   = "{{ cookiecutter.terraform_provider_hashicorp_aws_version }}"
    local = "{{ cookiecutter.terraform_provider_hashicorp_local_version }}"
  }
}