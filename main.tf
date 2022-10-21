terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
  client_id       = "0568731c-73ad-44fa-89b6-8123ee27d574"
  client_secret   = var.arm_client_secret
  tenant_id       = "7d6f97d6-d755-4c10-b763-409cc4b6638f"
}

data "azurerm_resource_group" "main" {
  name = "OpenCohort21_MatthewHolmes_ProjectExercise"
}

resource "random_string" "resource_code" {
  length  = 5
  special = false
  upper   = false
}

resource "azurerm_storage_account" "main" {
  name                     = "tfstate${random_string.resource_code.result}"
  resource_group_name      = data.azurerm_resource_group.main.name
  location                 = data.azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_nested_items_to_be_public = true

  tags = {
    environment = "production"
  }
}

resource "azurerm_storage_container" "main" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "mh-tf-todo-app-2022"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image     = "mholmesnominet/todo-app"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "CLIENT_ID" = var.client_id
    "CLIENT_SECRET" = var.client_secret
    "DATABASE" = azurerm_cosmosdb_mongo_database.main.name
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "DOCKER_ENABLE_CI" = true
    "ENDPOINT" = azurerm_cosmosdb_account.main.connection_strings[0]
    "SECRET_KEY" = var.secret_key
  }
}

resource "azurerm_cosmosdb_account" "main" {

  name                = "mh-module-12-todoapp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  capabilities {
    name = "EnableServerless"
  }

  # lifecycle {
  #   prevent_destroy = true
  # }

}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "mh-todoapp-2022"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
}