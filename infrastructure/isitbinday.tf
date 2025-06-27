resource "dokku_app" "api" {
  app_name = "isitbinday"

  domains = ["api.${var.domain}"]

  config = {
    DJANGO_SETTINGS_MODULE = "isitbinday.settings.production"
    ALLOWED_HOSTS          = "api.${var.domain}"
    BASE_URL               = "https://api.${var.domain}"
    AWS_ACCESS_KEY_ID      = "var.aws_access_key_id"
    AWS_SECRET_ACCESS_KEY  = "var.aws_secret_access_key"

    SMTP_PASS = aws_iam_access_key.access_key.ses_smtp_password_v4
    SMTP_USER = aws_iam_access_key.access_key.id
    SMTP_PORT = "587"
    SMTP_HOST = "email-smtp.${var.aws_region}.amazonaws.com"

    SECRET_KEY = var.secret_key
  }

  ports = {
    80 = {
      scheme         = "http"
      container_port = 8000
    }
  }
}

resource "dokku_plugin" "postgres" {
  name = "postgres"
  url  = "https://github.com/dokku/dokku-postgres.git"
}

resource "dokku_postgres" "main_db" {
  service_name = "api"
  image = "postgres:17.5"

  depends_on = [
    dokku_plugin.postgres
  ]
}

resource "dokku_postgres_link" "api_db_link" {
  app_name     = dokku_app.api.app_name
  service_name = dokku_postgres.main_db.service_name
  alias        = "DATABASE"

  depends_on = [
    dokku_plugin.postgres
  ]
}

output "git-remote" {
  value       = "dokku@${var.hosting_domain}:${dokku_app.api.app_name}"
  description = "Git remote"
  depends_on  = []
}
