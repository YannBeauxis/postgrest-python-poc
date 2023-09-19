resource "scaleway_container_namespace" "main" {
  project_id = var.project_id

  name        = "main"
  description = "Main container namespace"
  region      = local.region
}

data "scaleway_registry_namespace" "main" {
  namespace_id = scaleway_container_namespace.main.registry_namespace_id
}

# resource "scaleway_container" "dig" {
#   count = 10

#   name            = "dig-${count.index}"
#   namespace_id    = scaleway_container_namespace.main.id
#   registry_image  = "yannbeauxis/dig"
#   port            = 3001
#   cpu_limit       = 70
#   memory_limit    = 128
#   min_scale       = 0
#   max_scale       = 1
#   timeout         = 60
#   max_concurrency = 10
#   privacy         = "public"
#   deploy          = true

# }

resource "random_password" "pgrst_jwt_secret" {
  length  = 64
  special = false
  # override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "scaleway_secret" "pgrst_jwt_secret" {
  name        = "pgrst-jwt-secret"
  description = "Secret to generate JWT for PostgREST"
}

resource "scaleway_secret_version" "pgrst_jwt_secret" {
  description = "active"
  secret_id   = scaleway_secret.pgrst_jwt_secret.id
  data        = random_password.pgrst_jwt_secret.result
}

resource "scaleway_container" "postgrest" {
  name            = "postgrest"
  description     = "PostgREST API"
  namespace_id    = scaleway_container_namespace.main.id
  registry_image  = "postgrest/postgrest"
  port            = 3000
  cpu_limit       = 70
  memory_limit    = 128
  min_scale       = 0
  max_scale       = 1
  timeout         = 60
  max_concurrency = 10
  privacy         = "public"
  deploy          = true

  environment_variables = {
    "PGRST_DB_SCHEMAS"   = "api"
    "PGRST_DB_ANON_ROLE" = "web_anon"
  }
  secret_environment_variables = {
    "PGRST_DB_URI"     = local.sql_alchemy_url
    "PGRST_JWT_SECRET" = scaleway_secret_version.pgrst_jwt_secret.data
  }

  depends_on = [null_resource.db_migrate]
}

resource "scaleway_container" "auth_api" {
  name            = "auth-api"
  description     = "Auth API"
  namespace_id    = scaleway_container_namespace.main.id
  registry_image  = "yannbeauxis/ema_scraper_auth_api"
  port            = 8000
  cpu_limit       = 70
  memory_limit    = 128
  min_scale       = 0
  max_scale       = 1
  timeout         = 60
  max_concurrency = 10
  privacy         = "public"
  deploy          = true

  environment_variables = {

    "AUTH_API_ROLE" = "editor"
  }
  secret_environment_variables = {
    "MAGIC_API_SECRET_KEY" = var.MAGIC_API_SECRET_KEY
    "AUTH_API_SECRET_KEY"  = scaleway_secret_version.pgrst_jwt_secret.data
  }
}

resource "null_resource" "populate_data" {
  provisioner "local-exec" {
    command = "cd ../../../modules/ema-scraper && POSTGREST_CLIENT_SECRET_KEY=${random_password.pgrst_jwt_secret.result} EMA_SCRAPER_API_URL=https://${scaleway_container.postgrest.domain_name} poetry run python init_db.py"
  }
  depends_on = [scaleway_container.postgrest]
}
