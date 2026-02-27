#!/bin/bash
# Bulletproof EC2 Deployment Script for Slot Machine with MongoDB
# Run this script on your EC2 instance

set -e

echo "🚀 Starting deployment..."

# Configuration
IMAGE_NAME="keerti144/devops-game:latest"
APP_CONTAINER="slot-machine-app"
DB_CONTAINER="slot-machine-db"
NETWORK_NAME="app-network"

# Step 1: Clean up existing containers
echo "🧹 Cleaning up existing containers..."
docker stop $APP_CONTAINER 2>/dev/null || true
docker rm $APP_CONTAINER 2>/dev/null || true
docker stop $DB_CONTAINER 2>/dev/null || true
docker rm $DB_CONTAINER 2>/dev/null || true

# Step 2: Clean up network if it exists
echo "🌐 Setting up network..."
docker network rm $NETWORK_NAME 2>/dev/null || true
docker network create $NETWORK_NAME

# Step 3: Start MongoDB container
echo "🗄️  Starting MongoDB..."
docker run -d \
    --name $DB_CONTAINER \
    --network $NETWORK_NAME \
    -p 27017:27017 \
    --restart unless-stopped \
    -v mongo_data:/data/db \
    mongo:6

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to be ready..."
sleep 10

# Step 4: Pull latest application image
echo "📥 Pulling latest application image..."
docker pull $IMAGE_NAME

# Step 5: Start application container
echo "🎰 Starting application..."
docker run -d \
    --name $APP_CONTAINER \
    --network $NETWORK_NAME \
    -p 8000:8000 \
    --restart unless-stopped \
    -e MONGO_URI=mongodb://$DB_CONTAINER:27017 \
    $IMAGE_NAME

# Step 6: Verify deployment
echo "✅ Verifying deployment..."
sleep 5

if docker ps | grep -q $APP_CONTAINER && docker ps | grep -q $DB_CONTAINER; then
    echo ""
    echo "✅ ========================================="
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "✅ ========================================="
    echo ""
    echo "📱 Application: http://$(curl -s http://checkip.amazonaws.com):8000"
    echo "🗄️  MongoDB running on port 27017"
    echo ""
    echo "🔍 Container Status:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "slot-machine|NAMES"
    echo ""
    echo "📋 View logs with:"
    echo "   docker logs -f $APP_CONTAINER"
    echo "   docker logs -f $DB_CONTAINER"
else
    echo ""
    echo "❌ DEPLOYMENT FAILED!"
    echo "Check logs with:"
    echo "   docker logs $APP_CONTAINER"
    echo "   docker logs $DB_CONTAINER"
    exit 1
fi
