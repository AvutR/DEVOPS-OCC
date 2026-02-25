#!/bin/bash
# EC2 SSH Deployment Helper
# Automates SSH connection and deployment to EC2 instance

set -e

# Configuration
SSH_KEY_PATH="${SSH_KEY_PATH:-./.ssh/ec2-key.pem}"
SSH_USER="${SSH_USER:-ubuntu}"
EC2_IP="${EC2_IP}"
DEPLOY_SCRIPT="/opt/DEVOPS-OCC/infra/aws/deploy.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Validate inputs
if [ -z "$EC2_IP" ]; then
    print_error "EC2_IP environment variable not set"
    echo "Usage: EC2_IP=<instance-ip> SSH_USER=<user> ./deploy_ssh.sh"
    exit 1
fi

if [ ! -f "$SSH_KEY_PATH" ]; then
    print_error "SSH key not found at: $SSH_KEY_PATH"
    exit 1
fi

# Set SSH key permissions
chmod 600 "$SSH_KEY_PATH"
print_info "SSH key permissions set"

# Test SSH connection
print_info "Testing SSH connection to ${SSH_USER}@${EC2_IP}..."
if ! ssh -o ConnectTimeout=10 \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -i "$SSH_KEY_PATH" \
        "${SSH_USER}@${EC2_IP}" \
        "echo 'SSH connection successful'" ; then
    print_error "Failed to connect to EC2 instance"
    exit 1
fi
print_success "SSH connection test passed"

# Execute deployment
print_info "Starting deployment on ${EC2_IP}..."
ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -i "$SSH_KEY_PATH" \
    "${SSH_USER}@${EC2_IP}" \
    "bash ${DEPLOY_SCRIPT}"

if [ $? -eq 0 ]; then
    print_success "Deployment completed successfully!"
    echo ""
    print_info "API Available at:"
    echo "  http://${EC2_IP}:8000"
    echo "  Swagger UI: http://${EC2_IP}:8000/docs"
else
    print_error "Deployment failed"
    exit 1
fi
