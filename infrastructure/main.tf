terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.23.1"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
    dokku = {
      source  = "aliksend/dokku"
      version = "~> 1.0.14"
    }
    rollbar = {
      source  = "rollbar/rollbar"
      version = "~> 1.14.0"
    }
  }

  backend "s3" {
    encrypt = true
  }
}

variable "domain" {
  description = "Domain (no www)"
}

variable "repo" {
  description = "Git repository"
}

variable "email" {
  description = "Email address"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
}

variable "aws_region" {
  description = "AWS region"
}

variable "hosting_domain" {
  description = "Hosting domain"
}

variable "secret_key" {
  description = "Django secret key"
}

variable "zoneid" {
  description = "Cloudflare zone ID"
}

variable "rollbar_token" {
  description = "Rollbar API token"
}

variable "rollbar_project_token" {
  description = "Rollbar project token"
}

provider "aws" {
  region = var.aws_region
}

provider "dokku" {
  ssh_host = var.hosting_domain
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

provider "rollbar" {
  api_key         = var.rollbar_token
  project_api_key = var.rollbar_project_token
}
