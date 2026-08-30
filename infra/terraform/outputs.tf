output "service_url" {
  description = "Local URL for the learning service."
  value       = "http://localhost:${var.host_port}"
}

output "container_id" {
  description = "Docker container ID managed by Terraform."
  value       = docker_container.qe_fde_ai.id
}

