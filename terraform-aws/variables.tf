# Variables AWS
variable "region" {
  description = "Région AWS"
  type        = string
  default     = "eu-west-3"
}

variable "my_ip" {
  description = "Votre IP publique pour SSH (CIDR)"
  type        = string
}

variable "ssh_public_key_path" {
  description = "Chemin vers votre clé SSH publique"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}