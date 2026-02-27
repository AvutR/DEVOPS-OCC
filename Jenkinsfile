pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                cleanWs()
                checkout scm
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
                sh 'docker build --no-cache -t keerti144/devops-game:latest .'
                sh 'docker tag keerti144/devops-game:latest keerti144/devops-game:build-${BUILD_NUMBER}'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push keerti144/devops-game:latest'
                    sh 'docker push keerti144/devops-game:build-${BUILD_NUMBER}'
                }
            }
        }

        stage('Deploy to EC2') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying to EC2 instance via SSH...'
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    sh '''
                        chmod 600 ${SSH_KEY}
                        EC2_IP=${EC2_INSTANCE_IP}

                        if [ -z "$EC2_IP" ]; then
                            echo "Error: EC2_INSTANCE_IP not set"
                            exit 1
                        fi

                        ssh -o StrictHostKeyChecking=no \
                            -o UserKnownHostsFile=/dev/null \
                            -i ${SSH_KEY} \
                            ${SSH_USER}@${EC2_IP} \
                            "bash /opt/DEVOPS-OCC/infra/aws/deploy.sh"
                    '''
                }
            }
        }
    }
}