provider "azurerm" {
  features {}
}
resource "azurerm_resource_group" "churn" {
  name     = var.resource_group_name
  location = var.location
}
resource "azurerm_container_registry" "churn" {
  name                = var.registry_name
  resource_group_name = azurerm_resource_group.churn.name
  location            = azurerm_resource_group.churn.location
  sku                 = "Basic"
  admin_enabled       = false
}
output "registry_login_server" {
  value = azurerm_container_registry.churn.login_server
}
