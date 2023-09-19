module "root" {
  source = "../../modules/main"

  project_id           = "ed2a1db0-cac4-4acb-a61f-e9cbc41811be"
  MAGIC_API_SECRET_KEY = var.MAGIC_API_SECRET_KEY
}
