# EC2 Instance Outputs
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.qr_generator.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.qr_generator_eip.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.qr_generator.public_dns
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.qr_generator.private_ip
}

# Security Group Output
output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.qr_generator_sg.id
}

# Application URLs
output "backend_url" {
  description = "URL for the backend application"
  value       = "http://${aws_eip.qr_generator_eip.public_ip}:${var.backend_port}"
}

output "frontend_url" {
  description = "URL for the frontend application"
  value       = "http://${aws_eip.qr_generator_eip.public_ip}:${var.frontend_port}"
}

# SSH Access
output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_eip.qr_generator_eip.public_ip}"
}
