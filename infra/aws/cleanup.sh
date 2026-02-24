#!/bin/bash
# AWS EC2 Cleanup Script
# Removes EC2 instance and associated resources

set -e

echo "WARNING: This will delete all AWS EC2 resources for Slot Machine API"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Destroying Terraform infrastructure..."
cd "$(dirname "$0")"

terraform destroy -auto-approve

echo "Infrastructure cleanup complete!"
