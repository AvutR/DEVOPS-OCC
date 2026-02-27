OCC DevOps Slot Machine

A simple Vegas-style slot machine application built using FastAPI and deployed using Docker, Jenkins, and AWS EC2.

This project demonstrates containerization, CI/CD automation, Docker image versioning, and cloud deployment.

Project Overview

The application consists of:

A FastAPI backend

A static frontend (HTML)

Docker containerization

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

FastAPI

Uvicorn

Docker

Jenkins

AWS EC2

Project Structure
DEVOPS-OCC/
│
├── static/                # Frontend (index.html)
├── main.py                # FastAPI application
├── slot_engine.py         # Game logic
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── Jenkinsfile
API Endpoints

GET / – Serves frontend

GET /state – Returns game state

POST /spin – Spins the slot machine

POST /reset – Resets the game

Swagger documentation is available at:

http://<server-ip>:8000/docs
Running Locally (Docker)

Build and run:

docker compose up --build -d

Access the app at:

http://localhost:8000
Docker Image

Images are pushed to DockerHub with versioning:

keerti144/devops-game:latest

keerti144/devops-game:<build-number>

Example:

docker pull keerti144/devops-game:latest
docker run -d -p 8000:8000 keerti144/devops-game:latest
Deployment

The application is deployed on an AWS EC2 instance.

During deployment:

The latest Docker image is pulled from DockerHub

Existing container is stopped

New container is started on port 8000

Access:

http://<ec2-public-ip>:8000
Game Rules

Starting balance: $100

Each spin costs $5

Payouts:

7 7 7 → $1000

→ $500

# # → $250

$ $ $ → $200

@ @ @ → $150

License

MIT License
