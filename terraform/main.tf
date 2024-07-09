variable "gcp_project_id" {
  type        = string
  description = "The GCP project ID to apply this config to"
}

provider "google" {
  project = var.gcp_project_id
  region  = "europe-west3"
  zone    = "europe-west3-a"
}

resource "google_compute_instance" "default" {
  name         = "cloud-component-vm"
  machine_type = "e2-medium"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo docker pull yevheniikl/cloud_component
    sudo docker run -d -p 1883:1883 yevheniikl/cloud_component
  EOF
}

resource "google_compute_firewall" "default" {
  name    = "allow-mqtt"
  network = "default"

  allow {
    protocol = "tcp"
    ports = ["1883"]
  }

  source_ranges = ["0.0.0.0/0"]
}

