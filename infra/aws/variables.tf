# Terraform Variables for EC2 Deployment

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name of AWS EC2 Key Pair for SSH access"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}
