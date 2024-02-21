source "googlecompute" "my-img" {
  project_id          = var.project_id
  source_image_family = var.base_img_family
  zone                = var.img_zone
  image_name          = "${var.img_name}-${formatdate("h'h'mm", timestamp())}"
  ssh_username        = var.username
}
