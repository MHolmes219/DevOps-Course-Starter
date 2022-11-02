terraform {

  backend "azurerm" {
    resource_group_name  = "OpenCohort21_MatthewHolmes_ProjectExercise"
    storage_account_name = "tfstatev97g4"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }

  required_providers {
    
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.arm_client_secret
  tenant_id       = var.azure_tenant_id
}

data "azurerm_resource_group" "main" {
  name = "OpenCohort21_MatthewHolmes_ProjectExercise"
}

resource "random_string" "resource_code" {
  length  = 5
  special = false
  upper   = false
}

resource "azurerm_service_plan" "main" {
  name                = "mh-terraformed-asp"
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

  name                = "matth-module-12-todoapp"
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