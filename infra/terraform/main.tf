provider "docker" {}

resource "docker_image" "qe_fde_ai" {
  name = "qe-fde-ai:terraform"
  build {
    context = "${path.module}/../.."
  }
  keep_locally = true
}

resource "docker_container" "qe_fde_ai" {
  name  = "qe-fde-ai-learning"
  image = docker_image.qe_fde_ai.image_id

  env = [
    "FDE_API_KEY=${var.api_key}",
    "FDE_ENVIRONMENT=development",
    "FDE_MAX_DOCUMENTS=1000",
    "FDE_MAX_TOOL_STEPS=3"
  ]

  ports {
    internal = 8000
    external = var.host_port
  }

  read_only = true
  must_run  = true

  tmpfs = {
    "/tmp" = "rw,noexec,nosuid,size=64m"
  }

  healthcheck {
    test         = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
    interval     = "10s"
    timeout      = "3s"
    retries      = 3
    start_period = "10s"
  }
}

