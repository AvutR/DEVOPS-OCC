# EC2 Deployment Guide - Slot Machine with Authentication

## 🚀 Quick Deployment on EC2

### Prerequisites
- EC2 instance running (Ubuntu/Amazon Linux)
- Docker installed on EC2
- Security group allows ports: 22 (SSH), 8000 (App), 27017 (MongoDB)

### Step 1: SSH into EC2
```bash
ssh -i your-key.pem ubuntu@43.205.194.151
```

### Step 2: One-Command Deployment
```bash
curl -fsSL https://raw.githubusercontent.com/AvutR/DEVOPS-OCC/feature/auth-leaderboard/deploy_ec2.sh | bash
```

### Step 3: Manual Deployment (Alternative)
If you prefer manual control:

```bash
# 1. Pull the deployment script
wget https://raw.githubusercontent.com/AvutR/DEVOPS-OCC/feature/auth-leaderboard/deploy_ec2.sh

# 2. Make it executable
chmod +x deploy_ec2.sh

# 3. Run it
./deploy_ec2.sh
```

## 📋 Manual Deployment Steps

If the script doesn't work, follow these manual steps:

```bash
# 1. Stop existing containers
docker stop slot-machine-app slot-machine-db 2>/dev/null || true
docker rm slot-machine-app slot-machine-db 2>/dev/null || true

# 2. Create Docker network
docker network rm app-network 2>/dev/null || true
docker network create app-network

# 3. Start MongoDB
docker run -d \
    --name slot-machine-db \
    --network app-network \
    -p 27017:27017 \
    --restart unless-stopped \
    -v mongo_data:/data/db \
    mongo:6

# 4. Wait for MongoDB
sleep 10

# 5. Start Application
docker pull keerti144/devops-game:latest
docker run -d \
    --name slot-machine-app \
    --network app-network \
    -p 8000:8000 \
    --restart unless-stopped \
    -e MONGO_URI=mongodb://slot-machine-db:27017 \
    keerti144/devops-game:latest
```

## ✅ Verification

Check if containers are running:
```bash
docker ps
```

You should see both `slot-machine-app` and `slot-machine-db` running.

View application logs:
```bash
docker logs -f slot-machine-app
```

View MongoDB logs:
```bash
docker logs -f slot-machine-db
```

## 🌐 Access Your Application

Open in browser:
```
http://43.205.194.151:8000
```

## 🔄 Update/Redeploy

To deploy new version:
```bash
# Re-run the deployment script
./deploy_ec2.sh
```

Or manually:
```bash
docker pull keerti144/devops-game:latest
docker stop slot-machine-app
docker rm slot-machine-app
docker run -d \
    --name slot-machine-app \
    --network app-network \
    -p 8000:8000 \
    --restart unless-stopped \
    -e MONGO_URI=mongodb://slot-machine-db:27017 \
    keerti144/devops-game:latest
```

## 🐛 Troubleshooting

### App won't start
```bash
# Check logs
docker logs slot-machine-app

# Common fix - restart MongoDB first
docker restart slot-machine-db
sleep 5
docker restart slot-machine-app
```

### MongoDB connection issues
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Test MongoDB connection
docker exec -it slot-machine-db mongosh

# Check network
docker network inspect app-network
```

### Port already in use
```bash
# Find what's using the port
sudo lsof -i :8000

# Kill the old process
sudo kill -9 <PID>

# Then redeploy
```

### Clean slate (nuclear option)
```bash
# Remove everything
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network prune -f
docker volume prune -f

# Then run deployment script again
./deploy_ec2.sh
```

## 📊 Features

- ✅ User Registration & Login
- ✅ Password Authentication (bcrypt hashed)
- ✅ Global Leaderboard
- ✅ Per-user statistics
- ✅ Persistent data (MongoDB)
- ✅ Session management
- ✅ Auto-restart containers

## 🔒 Security Notes

- Passwords are hashed with bcrypt
- Uses secure token-based sessions
- MongoDB runs on internal network
- All data persisted in Docker volumes

## 📝 Environment Variables

The app uses these environment variables:
- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017)

## 💡 Tips

1. **Always check logs first** when something goes wrong
2. **MongoDB needs ~10 seconds** to start - don't rush it
3. **Use persistent volumes** to keep data across restarts
4. **Restart policy** ensures containers auto-restart on failure
