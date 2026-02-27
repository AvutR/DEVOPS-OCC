OCC DevOps Slot Machine

A full-featured Vegas-style slot machine application with user authentication, persistent game state, and leaderboard functionality. Built using FastAPI, MongoDB, and deployed using Docker, Jenkins, and AWS EC2.

This project demonstrates containerization, CI/CD automation, Docker image versioning, cloud deployment, and modern web application architecture with user management.

Project Overview

The application consists of:

A FastAPI backend with user authentication

MongoDB database for persistent storage

A responsive static frontend (HTML/CSS/JS)

User login/registration system

Per-user game state and statistics

Global leaderboard

Docker containerization with multi-service setup

Jenkins pipeline for automated builds

DockerHub image registry

AWS EC2 deployment

Every push to the master branch triggers:

Docker image build

Version tagging using Jenkins build number

Push to DockerHub

Deployment to EC2

Tech Stack

Python 3.11

FastAPI + Uvicorn

MongoDB 6

PyMongo

Passlib (password hashing with bcrypt)

Docker & Docker Compose

Jenkins

AWS EC2

Project Structure
DEVOPS-OCC/
│
├── static/                # Frontend (index.html)
│   └── index.html        # Full UI with login/register/game/leaderboard
├── main.py                # FastAPI application with auth endpoints
├── slot_engine.py         # Game logic
├── database.py            # MongoDB connection and collections
├── requirements.txt
├── Dockerfile
├── docker-compose.yml     # Multi-service setup (app + MongoDB)
└── Jenkinsfile

## Features

### 🔐 User Authentication
- **User Registration**: Create account with username (min 3 chars) and password (min 4 chars)
- **User Login**: Secure authentication with bcrypt password hashing
- **Session Management**: Token-based authentication with persistent sessions
- **User Logout**: Clean session termination

### 🎰 Game Features
- **Starting Balance**: Each new user starts with $100
- **Per-User Game State**: Each player has their own balance and game history
- **Spin Mechanics**: $5 per spin with various payout combinations
- **Win Tracking**: Real-time statistics for each player
- **Reset Protection**: Confirmation dialog before resetting balance to $100

### 📊 Statistics & Leaderboard
- **Personal Stats**: 
  - Total spins
  - Total wins
  - Total amount won
  - Win rate percentage
  - Highest single win
  - Maximum win streak
  - Last 5 spins history
- **Global Leaderboard**: View top 10 players ranked by balance
- **Real-time Updates**: Stats update after every spin

### 💾 Database Integration
- **MongoDB**: Persistent storage for all data
- **Collections**:
  - `users`: User accounts with hashed passwords and balances
  - `game_stats`: Per-user spin history and outcomes
- **Data Persistence**: All user data and game history saved across sessions

API Endpoints

### Authentication
- `POST /register` – Register new user
- `POST /login` – Login with credentials
- `POST /logout` – Logout and clear session

### Game
- `GET /` – Serves frontend
- `POST /spin` – Spin the slot machine (requires auth)
- `POST /reset` – Reset user's game to $100 (requires auth)
- `GET /stats` – Get user's game statistics (requires auth)
- `GET /leaderboard` – Get top 10 players (public)

Swagger documentation is available at:

http://<server-ip>:8000/docs

Running Locally (Docker Compose)

Build and run both services (app + MongoDB):

docker compose up --build -d

This will start:
- **MongoDB** on port 27017
- **Slot Machine App** on port 8000

Access the app at:

http://localhost:8000

To view logs:

docker compose logs -f

To stop:

docker compose down

Docker Image

Images are pushed to DockerHub with versioning:

keerti144/devops-game:latest

keerti144/devops-game:<build-number>

Example:

docker pull keerti144/devops-game:latest
docker run -d -p 8000:8000 keerti144/devops-game:latest

**Note**: When running standalone, ensure MongoDB is accessible via the `MONGO_URI` environment variable.

Deployment

The application is deployed on an AWS EC2 instance with Docker Compose.

During deployment:

The latest Docker image is pulled from DockerHub

Existing containers are stopped

New containers are started (app + MongoDB)

Access:

http://43.205.194.151:8000

Game Rules

Starting balance: $100

Each spin costs: $5

Payouts:

7 7 7 → $1000

→ $500

# # → $250

$ $ $ → $200

@ @ @ → $150

Reset: Sets balance back to $100 and clears user's history (requires confirmation)

Environment Variables

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017`)

Security Features

- **Password Hashing**: Bcrypt with salt for secure password storage
- **Token-Based Auth**: Secure session tokens for API authentication
- **User Isolation**: Each user's data is completely isolated
- **Input Validation**: Username and password requirements enforced

## Changelog (v3.0.0)

### Added
- ✅ User authentication system with registration and login
- ✅ MongoDB integration for persistent data storage
- ✅ User-specific game state and balance tracking
- ✅ Global leaderboard showing top 10 players
- ✅ Reset confirmation dialog to prevent accidental resets
- ✅ Per-user statistics and game history
- ✅ Session management with secure tokens
- ✅ Password hashing with bcrypt

### Changed
- ✅ Reset now sets balance to exactly $100 (not increment)
- ✅ All game operations are now user-specific
- ✅ Frontend redesigned with login/register screens
- ✅ Added tab navigation for Game and Leaderboard views

License

MIT License

