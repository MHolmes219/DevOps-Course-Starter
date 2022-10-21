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