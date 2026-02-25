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

        stage('Deploy to EC2') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying to EC2 instance via SSH...'
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    sh '''
                        # Set SSH key permissions
                        chmod 600 ${SSH_KEY}
                        
                        # Get EC2 instance IP from Terraform state or environment variable
                        EC2_IP=${EC2_INSTANCE_IP}
                        
                        if [ -z "$EC2_IP" ]; then
                            echo "Error: EC2_INSTANCE_IP not set"
                            exit 1
                        fi
                        
                        # Deploy via SSH
                        ssh -o StrictHostKeyChecking=no \
                            -o UserKnownHostsFile=/dev/null \
                            -i ${SSH_KEY} \
                            ${SSH_USER}@${EC2_IP} \
                            "bash /opt/DEVOPS-OCC/infra/aws/deploy.sh"
                        
                        echo "Deployment to EC2 (${EC2_IP}) completed successfully!"
                    '''
                }
            }
            post {
                success {
                    echo 'EC2 deployment successful!'
                }
                failure {
                    echo 'EC2 deployment failed!'
                }
            }
        }
    }
}