# OCC DevOps Slot Machine 🎰

A full-stack, containerized web application developed to demonstrate modern DevOps practices including CI/CD automation, Docker containerization, image versioning, and cloud deployment on AWS EC2.

**Live Application:**  
http://43.205.194.151:8000

**DockerHub Repository:** [keerti144/devops-game](https://hub.docker.com/r/keerti144/devops-game/tags)

---

## 📌 Project Overview

OCC DevOps Slot Machine is a three-tier web application that simulates a Vegas-style slot machine with secure user authentication, persistent game state, and a global leaderboard.

The project demonstrates:

- Backend API development using FastAPI
- Secure authentication with password hashing
- Persistent storage using MongoDB
- Containerization with Docker
- Multi-service orchestration
- Automated CI/CD using Jenkins
- Docker image versioning and registry management
- Cloud deployment on AWS EC2

---

## 🏗 System Architecture

The application follows a 3-tier architecture:

User Browser  
↓  
Frontend (HTML / CSS / JavaScript)  
↓  
FastAPI Backend (Docker Container)  
↓  
MongoDB Database (Docker Container)

### CI/CD Deployment Flow

GitHub Push  
→ Jenkins Pipeline Triggered  
→ Docker Image Built  
→ Image Tagged with Build Number  
→ Image Pushed to DockerHub  
→ EC2 Pulls Latest Image  
→ Containers Restart Automatically  

---

## 👥 User Stories

### Authentication

- As a new user, I want to register with a username and password so that I can create an account.
- As a registered user, I want to log in securely so that my balance and game history are preserved.
- As a user, I want my password securely hashed so that my account is protected.

### Gameplay

- As a player, I want to spin the slot machine so that I can attempt to win rewards.
- As a player, I want each spin to deduct $5 from my balance to simulate realistic gameplay.
- As a player, I want my balance updated immediately after each spin.
- As a player, I want confirmation before resetting my balance to avoid accidental data loss.

### Statistics & Leaderboard

- As a player, I want to view my total spins, wins, and win rate.
- As a player, I want to see my highest win and longest win streak.
- As a competitive player, I want to view a global leaderboard ranked by balance.

### Data Persistence

- As a user, I want my balance and game history stored permanently.
- As a user, I want my data isolated from other users.

### DevOps

- As a developer, I want every push to trigger an automated build.
- As a DevOps engineer, I want deployments automated to reduce manual errors.
- As a maintainer, I want versioned Docker images to allow rollback if needed.

---

## ⚙ Technology Stack

**Backend:**  
- Python 3.11  
- FastAPI  
- Uvicorn  

**Database:**  
- MongoDB 6  
- PyMongo  

**Authentication:**  
- Passlib (bcrypt hashing)  

**DevOps & Deployment:**  
- Docker  
- Docker Compose  
- Jenkins  
- DockerHub  
- AWS EC2  

---

## 🚀 Features

### 🔐 Authentication
- User registration
- Secure login/logout
- Password hashing using bcrypt
- Token-based session management

### 🎰 Game Engine
- Starting balance: $100
- Spin cost: $5
- Multiple payout combinations
- Reset confirmation protection
- Per-user balance tracking

### 📊 Statistics
- Total spins
- Total wins
- Win rate percentage
- Highest single win
- Maximum win streak
- Last 5 spins history

### 🏆 Leaderboard
- Top 10 players ranked by balance
- Real-time updates

---

## 💾 Database Design

### Collections

**users**
- username (unique index)
- hashed_password
- balance

**game_stats**
- username
- spin_result
- win_amount
- timestamp

MongoDB indexes ensure username uniqueness and efficient queries.

---

## 🐳 Running Locally
### Using Docker Compose
Build and run:
docker compose up --build -d

Services started:
- MongoDB → Port 27017
- Application → Port 8000

Access locally:
http://localhost:8000

Stop services:
docker compose down

---

## 📦 Docker Image
DockerHub Repository:
keerti144/devops-game

Pull latest image:
docker pull keerti144/devops-game:latest

Run manually:
docker run -d -p 8000:8000 keerti144/devops-game:latest

Note: When running standalone, ensure MongoDB is accessible using the `MONGO_URI` environment variable.
---

## 🔁 CI/CD Pipeline
On every push to the `master` branch:
1. Jenkins clones the repository.
2. Docker image is built.
3. Image is tagged using Jenkins build number.
4. Image is pushed to DockerHub.
5. Jenkins connects to EC2 via SSH.
6. EC2 pulls the latest image.
7. Existing containers are stopped.
8. New containers (app + MongoDB) are started.
Deployment is fully automated.

---
## ☁ Deployment
Hosted on AWS EC2.
Running Containers:
- `mongo-db`
- `slot-machine`

Live URL:
http://43.205.194.151:8000
---

## 🔐 Security Practices
- Bcrypt password hashing with salt
- Unique username enforcement
- Token-based authentication
- Environment variable-based configuration
- Per-user data isolation
---

## 🧪 DevOps Concepts Demonstrated
- Containerization
- Multi-service orchestration
- Automated CI/CD pipeline
- Versioned Docker images
- Cloud deployment
- Infrastructure automation
- Immutable deployment model
