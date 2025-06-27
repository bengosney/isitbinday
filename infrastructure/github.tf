locals {
  git_url = var.git_repository

  repo_name = regex("^.*[:/](.+)\\.git$", local.git_url)[0]
}

resource "tls_private_key" "deploy_key" {
  algorithm = "ED25519"
}

resource "github_actions_secret" "deploy_key" {
  repository      = local.repo_name
  secret_name     = "SSH_PRIVATE_KEY"
  plaintext_value = trimspace(join("", compact(split("\n", tls_private_key.deploy_key.private_key_openssh))))
}

output "deploy_public_key" {
  value = tls_private_key.deploy_key.public_key_openssh
  sensitive = false
}

resource "null_resource" "add_deploy_key" {
  provisioner "remote-exec" {
    connection {
      host        = var.hosting_domain
      user        = var.hosting_user
    }
    inline = [
      "echo '${tls_private_key.deploy_key.public_key_openssh}' >> ~/.ssh/authorized_keys"
    ]
  }
}