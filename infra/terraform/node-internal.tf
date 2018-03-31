resource "openstack_blockstorage_volume_v2" "internal-db-volume" {
  region      = "GRA1"
  name        = "internal-db"
  description = "PROD - Internal DB volume"
  size        = 10
  volume_type = "high-speed"
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

resource "openstack_compute_instance_v2" "internal-node-01" {
  name            = "internal-node-01.infra.insecurity-insa.fr"
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

resource "openstack_compute_instance_v2" "internal-node-02" {
  name            = "internal-node-02.infra.insecurity-insa.fr"
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

resource "openstack_compute_volume_attach_v2" "internal-db-01-volume-attach" {
  instance_id = "${openstack_compute_instance_v2.internal-db-01.id}"
  volume_id   = "${openstack_blockstorage_volume_v2.internal-db-volume.id}"
}

resource "ovh_domain_zone_record" "dns-internal-node-01-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "internal-node-01.infra"
  target    = "${openstack_compute_instance_v2.internal-node-01.network.0.fixed_ip_v4}"
  ttl       = 0
  depends_on = ["openstack_compute_instance_v2.internal-node-01"]
}

resource "ovh_domain_zone_record" "dns-internal-node-02-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "internal-node-02.infra"
  target    = "${openstack_compute_instance_v2.internal-node-02.network.0.fixed_ip_v4}"
  ttl       = 0
  depends_on = ["openstack_compute_instance_v2.internal-node-02"]
}

resource "ovh_domain_zone_record" "dns-internal-db-01-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "A"
  subdomain = "internal-db-01.infra"
  target    = "${openstack_compute_instance_v2.internal-db-01.network.0.fixed_ip_v4}"
  ttl       = 0
  depends_on = ["openstack_compute_instance_v2.internal-db-01"]
}

resource "ovh_domain_zone_record" "dns-internal-lb-01-infra-insecurity-insa-fr" {
  zone      = "insecurity-insa.fr"
  fieldtype = "CNAME"
  subdomain = "internal-lb.infra"
  target    = "internal-node-01.infra"
  ttl       = 0
}
