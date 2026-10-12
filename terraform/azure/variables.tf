variable "location" {
  type    = string
  default = "westeurope"
}
variable "resource_group_name" {
  type    = string
  default = "rg-ai-engineering-02"
}
variable "registry_name" {
  type        = string
  description = "Globally unique alphanumeric ACR name, 5-50 chars"
}
