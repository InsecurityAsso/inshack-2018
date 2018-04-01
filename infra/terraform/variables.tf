variable "openstack_tenant_id" {}
variable "openstack_tenant_name" {}
variable "openstack_username" {}
variable "openstack_password" {}
variable "openstack_region" {
    default = "GRA1"
}

variable "ovh_endpoint" {
    default = "ovh-eu"
}
variable "ovh_application_key" {}
variable "ovh_application_secret" {}
variable "ovh_consumer_key" {}

variable "prod_public_key" {}


variable "internal_node_count" {
    default = 2
}
variable "internal_lb_count" {
    default = 1
}
variable "chal_node_count" {
    default = 1
}
variable "privileged_node_count" {
    default = 1
}
