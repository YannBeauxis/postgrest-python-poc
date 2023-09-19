resource "random_password" "db_secret" {
  length           = 64
  special          = true
  override_special = "-_"
  min_special      = 1
}

resource "scaleway_secret" "db_secret" {
  name        = "db-secret"
  description = "Secret to connect to DB"
}

resource "scaleway_secret_version" "db_secret" {
  description = "active"
  secret_id   = scaleway_secret.db_secret.id
  data        = random_password.db_secret.result
}

resource "scaleway_rdb_instance" "main" {
  name           = "main"
  region         = local.region
  node_type      = "DB-DEV-S"
  engine         = "PostgreSQL-14"
  is_ha_cluster  = false
  disable_backup = true
}

resource "scaleway_rdb_user" "admin" {
  instance_id = scaleway_rdb_instance.main.id
  name        = "admin"
  password    = random_password.db_secret.result
  is_admin    = true
}
locals {
  db_info = scaleway_rdb_instance.main.load_balancer[0]
  # https://www.scaleway.com/en/docs/faq/serverless-containers/#can-i-allow-to-list-the-ips-of-my-containers
  allowed_ips = [
    "62.210.0.0/16",
    "195.154.0.0/16",
    "212.129.0.0/18",
    "62.4.0.0/19",
    "212.83.128.0/19",
    "212.83.160.0/19",
    "212.47.224.0/19",
    "163.172.0.0/16",
    "51.15.0.0/16",
    "151.115.0.0/16",
    "51.158.0.0/15",
  ]
  sql_alchemy_url = "postgresql://${scaleway_rdb_user.admin.name}:${random_password.db_secret.result}@${local.db_info.ip}:${local.db_info.port}/ema-scrapper"
}

resource "scaleway_rdb_acl" "main" {
  instance_id = scaleway_rdb_instance.main.id
  acl_rules {
    ip          = "82.121.223.95/32"
    description = "Yann's Home IP"
  }

  acl_rules {
    ip          = "100.64.5.163/32"
    description = "Scaleway internal IP"
  }

  dynamic "acl_rules" {
    for_each = local.allowed_ips
    content {
      ip          = acl_rules.value
      description = "Scaleway container's IP"
    }
  }

  # acl_rules {
  #   ip          = "0.0.0.0/0"
  #   description = "All IP"
  # }

}


resource "scaleway_rdb_database" "herbaltea_classifier" {
  instance_id = scaleway_rdb_instance.main.id
  name        = "ema-scrapper"
}

resource "scaleway_rdb_privilege" "herbaltea_classifier" {
  instance_id   = scaleway_rdb_instance.main.id
  user_name     = scaleway_rdb_user.admin.name
  database_name = scaleway_rdb_database.herbaltea_classifier.name
  permission    = "all"

}

resource "null_resource" "db_migrate" {
  provisioner "local-exec" {
    command = "cd ../../../api/crud && SQL_ALCHEMY_URL=${local.sql_alchemy_url} poetry run alembic upgrade head"
  }
  depends_on = [scaleway_rdb_privilege.herbaltea_classifier]
}
