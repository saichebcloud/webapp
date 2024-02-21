variable project_id {
  type    = string
  default = "devp-414719"
}

variable base_img_family {
  type    = string
  default = "centos-stream-8"
}

variable img_zone {
  type    = string
  default = "us-central1-a"
}

variable img_name {
  type    = string
  default = "custom-img"
}

variable username {
  type    = string
  default = "centos"
}

variable archive_path {
  type    = string
  default = ""
}