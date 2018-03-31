data "openstack_compute_flavor_v2" "vps-ssd-1" {
  vcpus = 1
  ram   = 2000
}

data "openstack_compute_flavor_v2" "vps-ssd-2" {
  vcpus = 1
  ram   = 4000
}

data "openstack_compute_flavor_v2" "vps-ssd-3" {
  vcpus = 2
  ram   = 8000
}
