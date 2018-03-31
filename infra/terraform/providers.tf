provider "ovh" {
  endpoint           = "${var.ovh_endpoint}"
  application_key    = "${var.ovh_application_key}"
  application_secret = "${var.ovh_application_secret}"
  consumer_key       = "${var.ovh_consumer_key}"
}

provider "openstack" {
  user_name   = "${var.openstack_username}"
  tenant_name = "${var.openstack_tenant_name}"
  tenant_id   = "${var.openstack_tenant_id}"
  password    = "${var.openstack_password}"
  auth_url    = "https://auth.cloud.ovh.net/v2.0"
  region      = "GRA1"
}

resource "openstack_compute_keypair_v2" "prod-keypair" {
  name       = "prod-keypair"
  public_key = "${var.prod_public_key}"
}
