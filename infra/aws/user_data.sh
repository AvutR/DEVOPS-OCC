#!/bin/bash
# AWS EC2 User Data Script - Initial Setup
# This runs when the EC2 instance is first launched

set -e

echo "Starting EC2 instance setup..."

# Update system packages
apt-get update
apt-get upgrade -y

# Install Python and dependencies
apt-get install -y python3 python3-pip python3-venv git curl

# Install Docker
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone the repository
cd /opt
git clone https://github.com/AvutR/DEVOPS-OCC.git
cd DEVOPS-OCC

# Create environment file
cat > .env << EOF
FLASK_ENV=production
FLASK_APP=main.py
DEBUG=False
EOF

echo "EC2 instance setup complete!"
