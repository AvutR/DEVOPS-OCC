# Jenkins EC2 SSH Deployment Configuration

Guide to configure Jenkins for automated EC2 SSH deployment.

## Prerequisites

- EC2 instance deployed (using `infra/aws/main.tf`)
- EC2 SSH key pair (.pem file)
- Jenkins with SSH plugin installed
- SSH Agent plugin installed

## Jenkins Setup Steps

### 1. Add SSH Credentials to Jenkins

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Credentials**
2. Click **Global** → **Add Credentials**
3. Select: **SSH Username with private key**
4. Fill in:
   - **ID**: `ec2-ssh-key`
   - **Description**: EC2 Deployment SSH Key
   - **Username**: `ubuntu` (default Ubuntu AMI user)
   - **Private Key**: Paste the contents of your `.pem` file (or upload)
5. Click **Create**

### 2. Configure EC2 Instance IP

Option A: Jenkins Global Variable
1. Go to **Manage Jenkins** → **Configure System**
2. Scroll to **Global properties** → **Environment variables**
3. Add new variable:
   - **Name**: `EC2_INSTANCE_IP`
   - **Value**: Your EC2 public IP (e.g., `54.123.45.67`)
4. Save

Option B: Jenkins Job Parameter
1. In your Jenkins job, enable **This project is parameterized**
2. Add **String Parameter**:
   - **Name**: `EC2_INSTANCE_IP`
   - **Default Value**: Your EC2 IP
3. Save

Option C: Terraform State (Automated)
1. Use Terraform output variables:
   ```bash
   echo "export EC2_INSTANCE_IP=$(terraform output -raw instance_ip)" >> /var/jenkins_home/.bashrc
   ```

### 3. Install Required Jenkins Plugins

- **SSH Agent Plugin** - For SSH key handling
- **Pipeline plugin** - For Declarative Pipeline
- **Docker Pipeline** - For Docker integration

Install via: **Manage Jenkins** → **Manage Plugins** → **Available**

## Pipeline Execution Flow

```
Clone → Build → Docker Build → Docker Push → Deploy to EC2
                                               ↓
                                      (Only on master branch)
                                      SSH into EC2
                                      Run deploy.sh
                                      Verify containers
```

## Manual Deployment (without Jenkins)

```bash
# Set environment variables
export EC2_INSTANCE_IP="your-instance-ip"
export SSH_USER="ubuntu"
export SSH_KEY_PATH="/path/to/ec2-key.pem"

# Run deployment
bash infra/aws/deploy_ssh.sh
```

## Troubleshooting

### SSH Connection Timeout
- Verify Security Group allows port 22 from your IP
- Check EC2 instance is running: `aws ec2 describe-instances`
- Test manually: `ssh -i key.pem ubuntu@<ip>`

### Permission Denied (PublicKey)
- Ensure SSH key has correct permissions: `chmod 600 key.pem`
- Verify key pair name matches instance

### Deployment Script Not Found
- Confirm `/opt/DEVOPS-OCC/infra/aws/deploy.sh` exists on instance
- SSH into instance and verify: `ls -la /opt/DEVOPS-OCC/`

### Docker Containers Not Starting
- SSH into EC2: `ssh -i key.pem ubuntu@<ip>`
- Check logs: `docker-compose logs -f`
- Verify environment: `docker-compose ps`

## Security Best Practices

1. **Restrict SSH Access**
   - In Security Group, restrict SSH to Jenkins server IP only
   - Use CIDR: `Jenkins-IP/32` instead of `0.0.0.0/0`

2. **Rotate SSH Keys Regularly**
   - Store keys in Jenkins secret management, not in repo

3. **Use Jenkins Agent Nodes**
   - Run deployment on dedicated agent for isolation
   - Add in Jenkinsfile: `agent { label 'deployment' }`

4. **Monitor Deployments**
   - Check Jenkins logs: **Manage Jenkins** → **System Log**
   - SSH into EC2 and monitor: `docker-compose logs -f`

5. **Backup State**
   - Store Terraform state in S3 with versioning:
     ```hcl
     terraform {
       backend "s3" {
         bucket         = "your-state-bucket"
         key            = "slot-machine/terraform.tfstate"
         region         = "us-east-1"
         encrypt        = true
         dynamodb_table = "terraform-locks"
       }
     }
     ```

## Environment Variables Summary

| Variable | Description | Example |
|----------|-------------|---------| 
| `EC2_INSTANCE_IP` | Public IP of target EC2 | `54.123.45.67` |
| `SSH_USER` | SSH username | `ubuntu` |
| `SSH_KEY` | Jenkins credential ID | `ec2-ssh-key` |
| `DEPLOY_SCRIPT` | Path to deploy script on EC2 | `/opt/DEVOPS-OCC/infra/aws/deploy.sh` |

## Pipeline Status Checks

After deployment, verify:

```bash
# Check API is responding
curl http://EC2_IP:8000/state

# Check containers are running
ssh -i key.pem ubuntu@EC2_IP "docker-compose ps"

# Check logs
ssh -i key.pem ubuntu@EC2_IP "docker-compose logs -f"
```

## Next Steps

1. Create Jenkins job from Jenkinsfile in repo
2. Configure EC2 SSH credentials
3. Set EC2_INSTANCE_IP environment variable
4. Run initial deployment manually to verify
5. Enable automatic deployment on master branch commits
