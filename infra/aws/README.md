# AWS EC2 Deployment Guide

Deploy the Vegas Slot Machine API to AWS EC2 using Infrastructure as Code and automated deployment scripts.

## Prerequisites

- AWS Account with appropriate permissions
- Terraform installed (v1.0+)
- AWS CLI configured with credentials
- EC2 Key Pair created in AWS

## Files

- **user_data.sh** - EC2 initialization script (runs on instance launch)
- **deploy.sh** - Deployment script (pulls code and starts containers)
- **main.tf** - Terraform EC2 and security group configuration
- **variables.tf** - Terraform variables
- **data.tf** - Terraform data sources (Ubuntu AMI lookup)
- **cleanup.sh** - Destroys infrastructure

## Quick Start

### 1. Configure Variables

Create `terraform.tfvars`:
```hcl
aws_region    = "us-east-1"
instance_type = "t3.micro"
key_pair_name = "your-ec2-key-pair"
environment   = "production"
```

### 2. Deploy Infrastructure

```bash
cd infra/aws
terraform init
terraform plan
terraform apply
```

### 3. Get Access

After deployment, Terraform outputs the API URL and SSH command:
```bash
ssh -i /path/to/key.pem ubuntu@<instance-ip>
curl http://<instance-ip>:8000/
```

### 4. Manual Deployment (if needed)

Connect to instance and run:
```bash
bash /opt/DEVOPS-OCC/infra/aws/deploy.sh
```

### 5. Cleanup

```bash
terraform destroy
# or use the cleanup script
bash cleanup.sh
```

## API Endpoints

Once deployed, access the API:

- `GET http://<instance-ip>:8000/` - Welcome
- `GET http://<instance-ip>:8000/state` - Game state
- `POST http://<instance-ip>:8000/spin` - Spin reels
- `POST http://<instance-ip>:8000/reset` - Reset game
- `GET http://<instance-ip>:8000/docs` - Swagger UI

## Monitoring

SSH into the instance and check logs:
```bash
sudo docker-compose ps
sudo docker-compose logs -f
tail -f /var/log/slot-machine-deploy.log
```

## Cost Optimization

- Using `t3.micro` for free tier eligibility
- Consider setting up Auto Scaling Groups for production
- Use CloudWatch for monitoring and alerts

## Security Notes

- Security group allows SSH (22) and HTTP (8000) from anywhere
- For production, restrict SSH to your IP: `cidr_blocks = ["YOUR_IP/32"]`
- Consider using HTTPS with ALB and ACM certificates
