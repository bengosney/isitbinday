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
      version = "~> 1.0.24"
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

variable "hosting_user" {
  description = "SSH user for hosting"
}

variable "secret_key" {
  description = "Django secret key"
}

variable "zoneid" {
  description = "Cloudflare zone ID"
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
