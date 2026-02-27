pipeline {
    agent any

    environment {
        IMAGE_NAME = "keerti144/devops-game"
        EC2_INSTANCE_IP = "43.205.194.151"
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build --no-cache -t $IMAGE_NAME:${BUILD_NUMBER} .
                docker tag $IMAGE_NAME:${BUILD_NUMBER} $IMAGE_NAME:latest
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:${BUILD_NUMBER}
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            when {
                expression {
                    return env.GIT_BRANCH?.endsWith('/master')
                }
            }
            steps {
                sshagent(['ec2-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@$EC2_INSTANCE_IP '
                        docker pull $IMAGE_NAME:latest
                        docker stop slot-machine 2>/dev/null || true
                        docker rm slot-machine 2>/dev/null || true
                        docker run -d -p 8000:8000 --name slot-machine $IMAGE_NAME:latest
                    '
                    """
                }
            }
        }
    }
}
