# AWS EC2 Infrastructure as Code - Terraform
# Provisions EC2 instance for Slot Machine API

terraform {
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

# Security Group
resource "aws_security_group" "slot_machine" {
  name        = "slot-machine-sg"
  description = "Security group for Slot Machine API"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "slot-machine-sg"
  }
}

# EC2 Instance
resource "aws_instance" "slot_machine" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.slot_machine.id]
  user_data              = file("${path.module}/user_data.sh")

  tags = {
    Name = "slot-machine-api"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Outputs
output "instance_ip" {
  value       = aws_instance.slot_machine.public_ip
  description = "Public IP of EC2 instance"
}

output "api_url" {
  value       = "http://${aws_instance.slot_machine.public_ip}:8000"
  description = "API endpoint URL"
}

output "ssh_command" {
  value       = "ssh -i /path/to/key.pem ubuntu@${aws_instance.slot_machine.public_ip}"
  description = "SSH command to connect to instance"
}
