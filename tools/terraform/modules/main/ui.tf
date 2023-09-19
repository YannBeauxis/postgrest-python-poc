
resource "null_resource" "build_admin_ui" {
  provisioner "local-exec" {
    command = "cd ../../../ui/admin && REACT_APP_AUTH_API_URL=https://${scaleway_container.auth_api.domain_name} REACT_APP_DATA_API_URL=https://${scaleway_container.postgrest.domain_name} npm run build && surge build https://admin-ema-scraper.surge.sh"
  }
  depends_on = [scaleway_rdb_privilege.herbaltea_classifier, scaleway_container.auth_api]
}

resource "null_resource" "build_public_ui" {
  provisioner "local-exec" {
    command = "cd ../../../ui/public && REACT_APP_DATA_API_URL=https://${scaleway_container.postgrest.domain_name} npm run build && surge build public.ema-scraper.surge.sh"
  }
  depends_on = [scaleway_rdb_privilege.herbaltea_classifier]
}
