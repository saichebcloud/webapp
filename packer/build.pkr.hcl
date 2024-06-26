build {
  sources = ["sources.googlecompute.my-img"]

  provisioner "shell" {
    script = "./scripts/user.sh"
  }

  provisioner "file" {
    source      = var.archive_path
    destination = "/tmp/Archive.zip"
  }

  provisioner "file" {
    source      = "./webapp.service"
    destination = "/tmp/webapp.service"
  }

  provisioner "shell" {
    script = "./scripts/system_installations.sh"
  }

  provisioner "shell" {
    script = "./scripts/unzip_and_install_pydeps.sh"
  }

  provisioner "shell" {
    script = "./scripts/install_ops_agent.sh"
  }

  provisioner "shell" {
    script = "./scripts/generate_ops_agent_config_file.sh"
  }

  provisioner "shell" {
    script = "./scripts/move_code.sh"
  }

  provisioner "shell" {
    script = "./scripts/change_ownership.sh"
  }

  provisioner "shell" {
    script = "./scripts/enable_services.sh"
  }

}
