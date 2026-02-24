pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Repo already cloned by Jenkins'
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'pip install -r requirements.txt || true'
                sh 'npm install || true'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t keerti144/devops-game:latest .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push keerti144/devops-game:latest'
                }
            }
        }
    }
}