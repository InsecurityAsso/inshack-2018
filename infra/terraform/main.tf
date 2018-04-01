# Persistent volumes
resource "openstack_blockstorage_volume_v2" "rancher-server-volume" {
  region      = "GRA1"
  name        = "rancher-server"
  description = "PROD - Rancher server volume"
  size        = 10
  volume_type = "high-speed"
}
resource "openstack_blockstorage_volume_v2" "internal-db-volume" {
  region      = "GRA1"
  name        = "internal-db"
  description = "PROD - Internal DB volume"
  size        = 10
  volume_type = "high-speed"
}

# Compute instances
resource "openstack_compute_instance_v2" "rancher-server" {
  name            = "rancher.infra.insecurity-insa.fr"
  image_id        = "07c6c63d-4836-4a43-ac46-5c7108a63940"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-2.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}
resource "openstack_compute_instance_v2" "management" {
  name            = "mgmt.infra.insecurity-insa.fr"
  image_id        = "d44515bd-8d5a-47bc-bc17-23fa4c238548"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-1.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}
resource "openstack_compute_instance_v2" "internal-db-01" {
  name            = "internal-db-01.infra.insecurity-insa.fr"
  image_id        = "d44515bd-8d5a-47bc-bc17-23fa4c238548"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-1.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}
resource "openstack_compute_instance_v2" "internal-node" {
  count           = "${var.internal_node_count}"
  name            = "${format("internal-node-%02d.infra.insecurity-insa.fr", count.index + 1)}"
  image_id        = "d44515bd-8d5a-47bc-bc17-23fa4c238548"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-2.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}
resource "openstack_compute_instance_v2" "privileged-node" {
  count           = "${var.privileged_node_count}"
  name            = "${format("privileged-node-%02d.infra.insecurity-insa.fr", count.index + 1)}"
  image_id        = "d44515bd-8d5a-47bc-bc17-23fa4c238548"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-3.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}
resource "openstack_compute_instance_v2" "chal-node" {
  count           = "${var.chal_node_count}"
  name            = "${format("chal-node-%02d.infra.insecurity-insa.fr", count.index + 1)}"
  image_id        = "d44515bd-8d5a-47bc-bc17-23fa4c238548"
  flavor_id       = "${data.openstack_compute_flavor_v2.vps-ssd-1.id}"
  key_pair        = "${openstack_compute_keypair_v2.prod-keypair.name}"
  security_groups = ["default"]
  region          = "GRA1"

  network {
    name = "Ext-Net"
  }

  depends_on = ["openstack_compute_keypair_v2.prod-keypair"]
}


# Instances <-> volume links
resource "openstack_compute_volume_attach_v2" "rancher-master-volume-attach" {
  instance_id = "${openstack_compute_instance_v2.rancher-server.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.rancher-server-volume.id}"
}
resource "openstack_compute_volume_attach_v2" "internal-db-01-volume-attach" {
  instance_id = "${openstack_compute_instance_v2.internal-db-01.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.internal-db-volume.id}"
}


# DNS configuration
resource "ovh_domain_zone_record" "dns-rancher-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "rancher.infra"
  target    = "${openstack_compute_instance_v2.rancher-server.network.0.fixed_ip_v4}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.rancher-server"]
}
resource "ovh_domain_zone_record" "dns-management-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "mgmt.infra"
  target    = "${openstack_compute_instance_v2.management.network.0.fixed_ip_v4}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.management"]
}
resource "ovh_domain_zone_record" "dns-munin-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "CNAME"
  subdomain = "munin.infra"
  target    = "mgmt.infra"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.management"]
}
resource "ovh_domain_zone_record" "dns-internal-db-01-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "internal-db-01.infra"
  target    = "${openstack_compute_instance_v2.internal-db-01.network.0.fixed_ip_v4}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.internal-db-01"]
}
resource "ovh_domain_zone_record" "dns-internal-lb-01-infra-insecurity-insa-fr" {
  count     = "${var.internal_lb_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "CNAME"
  subdomain = "internal-lb.infra"
  target    = "${format("internal-node-%02d.infra", count.index + 1)}"
  ttl       = 120
}
resource "ovh_domain_zone_record" "dns-internal-node" {
  count     = "${var.internal_node_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "${format("internal-node-%02d.infra", count.index + 1)}"
  target    = "${element(openstack_compute_instance_v2.internal-node.*.network.0.fixed_ip_v4, count.index)}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.internal-node"]
}
resource "ovh_domain_zone_record" "dns-privileged-node" {
  count     = "${var.privileged_node_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "${format("privileged-node-%02d.infra", count.index + 1)}"
  target    = "${element(openstack_compute_instance_v2.privileged-node.*.network.0.fixed_ip_v4, count.index)}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.privileged-node"]
}
resource "ovh_domain_zone_record" "dns-privileged-lb" {
  count     = "${var.privileged_node_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "CNAME"
  subdomain = "privileged-lb.infra"
  target    = "${format("privileged-node-%02d.infra", count.index + 1)}"
  ttl       = 120
}
resource "ovh_domain_zone_record" "dns-chal-node" {
  count     = "${var.chal_node_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "${format("chal-node-%02d.infra", count.index + 1)}"
  target    = "${element(openstack_compute_instance_v2.chal-node.*.network.0.fixed_ip_v4, count.index)}"
  ttl       = 120
  depends_on = ["openstack_compute_instance_v2.chal-node"]
}

resource "ovh_domain_zone_record" "dns-chal-lb" {
  count     = "${var.chal_node_count}"
  zone      = "insecurity-insa.fr"
  fieldtype = "CNAME"
  subdomain = "chal-lb.infra"
  target    = "${format("chal-node-%02d.infra", count.index + 1)}"
  ttl       = 120
}
