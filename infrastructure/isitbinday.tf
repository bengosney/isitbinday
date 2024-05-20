resource "dokku_app" "api" {
  app_name = "isitbinday"

  domains = [var.domain]

  ports = {
    80 = {
      scheme         = "http"
      container_port = 8000
    }
  }
}

resource "dokku_postgres" "main_db" {
  service_name = "api"
}

resource "dokku_postgres_link" "api_db_link" {
  app_name     = dokku_app.api.app_name
  service_name = dokku_postgres.main_db.service_name
  alias        = "DATABASE"
}
