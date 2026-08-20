# ============================================================
# Configuration Terraform - Amazon Web Services (AWS)
# Projet : TopGainersCryptoProject
# Compte : Free Tier (535510333060)
# ============================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# ============ RÉSEAU ============

# VPC principal
resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "topgainers-vpc"
  }
}

# Subnet public
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.region}a"

  tags = {
    Name = "topgainers-public-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main_igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "topgainers-igw"
  }
}

# Route Table publique
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_igw.id
  }

  tags = {
    Name = "topgainers-public-rt"
  }
}

# Association Subnet <-> Route Table
resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group
resource "aws_security_group" "main_sg" {
  name        = "topgainers-sg"
  description = "Security group pour TopGainersCrypto"
  vpc_id      = aws_vpc.main_vpc.id

  # SSH (port 22) - restreint à l'IP admin
  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["${var.my_ip}/32"]
  }

  # Application Streamlit (port 8501)
  ingress {
    protocol    = "tcp"
    from_port   = 8501
    to_port     = 8501
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus (port 9090)
  ingress {
    protocol    = "tcp"
    from_port   = 9090
    to_port     = 9090
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Grafana (port 3000)
  ingress {
    protocol    = "tcp"
    from_port   = 3000
    to_port     = 3000
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Trafic sortant
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "topgainers-sg"
  }
}

# ============ INSTANCE EC2 ============
# t3.micro : 1 vCPU / 1 GB RAM - Free Tier AWS (750h/mois pendant 12 mois)
# Optimisé pour Docker + PostgreSQL + Prometheus + Grafana avec limites de mémoire

resource "aws_instance" "topgainers_vm" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.main_sg.id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.deploy_key.key_name

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "topgainers-vm"
  }
}

# ============ CLÉ SSH ============

resource "aws_key_pair" "deploy_key" {
  key_name   = "topgainers-deploy-key"
  public_key = file(var.ssh_public_key_path)
}

# ============ DONNÉES ============

# Dernière AMI Ubuntu 22.04
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}
