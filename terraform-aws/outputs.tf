# Sorties Terraform AWS
output "instance_public_ip" {
  description = "IP publique de l'instance EC2"
  value       = aws_instance.topgainers_vm.public_ip
}

output "instance_id" {
  description = "ID de l'instance EC2"
  value       = aws_instance.topgainers_vm.id
}

output "vpc_id" {
  description = "ID du VPC"
  value       = aws_vpc.main_vpc.id
}

output "app_url" {
  description = "URL de l'application Streamlit"
  value       = "http://${aws_instance.topgainers_vm.public_ip}:8501"
}

output "prometheus_url" {
  description = "URL de Prometheus"
  value       = "http://${aws_instance.topgainers_vm.public_ip}:9090"
}

output "grafana_url" {
  description = "URL de Grafana"
  value       = "http://${aws_instance.topgainers_vm.public_ip}:3000"
}