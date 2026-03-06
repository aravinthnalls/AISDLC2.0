# AWS Configuration Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "production"
}

# EC2 Configuration
variable "ami_id" {
  description = "AMI ID for EC2 instance"
  type        = string
  default     = "ami-0c7217cdde317cfec" # Ubuntu 22.04 LTS
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "Name of the AWS key pair for EC2 access"
  type        = string
}

# Application Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "qr-generator"
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "Qr-Generator"
    ManagedBy   = "Terraform"
    Environment = "production"
  }
}

# Application Port Configuration
variable "frontend_port" {
  description = "Port for the frontend application"
  type        = number
  default     = 3000
}

variable "backend_port" {
  description = "Port for the backend application"  
  type        = number
  default     = 8000
}

# Deployment Configuration
variable "deploy_method" {
  description = "Deployment method (docker-compose, kubernetes, etc.)"
  type        = string
  default     = "docker-compose"
}

variable "target_platform" {
  description = "Target deployment platform"
  type        = string
  default     = "aws_ec2"
}
