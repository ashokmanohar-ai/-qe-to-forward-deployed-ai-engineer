variable "api_key" {
  description = "Local disposable API key. Supply through TF_VAR_api_key; do not commit it."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.api_key) >= 16
    error_message = "api_key must contain at least 16 characters."
  }
}

variable "host_port" {
  description = "Local host port for the learning service."
  type        = number
  default     = 8000

  validation {
    condition     = var.host_port >= 1024 && var.host_port <= 65535
    error_message = "host_port must be between 1024 and 65535."
  }
}

