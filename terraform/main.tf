# AWS Provider configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Security group for the application
resource "aws_security_group" "qr_generator_sg" {
  name_prefix = "qr-generator-"
  description = "Security group for QR Generator application"
  
  # Allow HTTP traffic
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Allow HTTPS traffic
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp" 
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Allow SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Allow backend port
  ingress {
    from_port   = var.backend_port
    to_port     = var.backend_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Allow frontend port
  ingress {
    from_port   = var.frontend_port
    to_port     = var.frontend_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "qr-generator-security-group"
    Project = "QR Generator"
  }
}

# EC2 Instance for the application
resource "aws_instance" "qr_generator" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name
  
  vpc_security_group_ids = [aws_security_group.qr_generator_sg.id]
  
  # User data script to set up the application
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    backend_port  = var.backend_port
    frontend_port = var.frontend_port
  }))
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }
  
  tags = merge(var.tags, {
    Name = "${var.project_name}-instance"
    Type = "application-server"
  })
}

# Elastic IP for the instance
resource "aws_eip" "qr_generator_eip" {
  instance = aws_instance.qr_generator.id
  domain   = "vpc"
  
  tags = {
    Name = "qr-generator-eip"
    Project = "QR Generator"
  }
}
