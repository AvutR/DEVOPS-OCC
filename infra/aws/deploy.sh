#!/bin/bash
# AWS EC2 Deployment Script
# Pulls latest code and deploys using Docker Compose

set -e

APP_DIR="/opt/DEVOPS-OCC"
LOG_FILE="/var/log/slot-machine-deploy.log"

echo "$(date) - Starting deployment..." | tee -a $LOG_FILE

# Navigate to app directory
cd $APP_DIR

# Pull latest changes from master
echo "Pulling latest code from GitHub..." | tee -a $LOG_FILE
git fetch origin
git checkout master
git pull origin master

# Build and start Docker containers
echo "Building and starting Docker containers..." | tee -a $LOG_FILE
docker-compose build --no-cache
docker-compose down
docker-compose up -d

# Verify containers are running
echo "Verifying deployment..." | tee -a $LOG_FILE
if docker-compose ps | grep -q "Up"; then
    echo "$(date) - Deployment successful!" | tee -a $LOG_FILE
    echo "API available at: http://$(hostname -I | awk '{print $1}'):8000"
else
    echo "$(date) - Deployment FAILED!" | tee -a $LOG_FILE
    exit 1
fi
