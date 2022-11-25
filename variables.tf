variable "client_id" {
  description = "The oAuth client ID value for connection"
}

variable "client_secret" {
  description = "The oAuth client secret value for connection"
  sensitive = true
}

variable "secret_key" {
    description = "The secret key value"
    sensitive = true
}

variable "azure_client_secret" {
  description = "The client secret value for azure connection"
  sensitive = true
}

variable "azure_client_id" {
  description = "The client ID for the azure provider"
}

variable "azure_subscription_id" {
  description = "The subscription ID for the azure provider"
}

variable "azure_tenant_id" {
  description = "The tenant ID for the azure provider"
}