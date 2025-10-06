#!/bin/bash
set -e

# Update system
yum update -y

# Install Docker
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
yum install git -y

# Create application directory
mkdir -p /opt/qr-generator
cd /opt/qr-generator

# Clone the repository (this would be updated with actual repo URL)
# git clone https://github.com/your-username/qr-generator.git .

# For now, create a simple deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
echo "Starting QR Generator application..."

# Start services with Docker Compose
docker-compose up -d

# Show status
docker-compose ps

echo "Application deployed successfully!"
echo "Backend available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${backend_port}"
echo "Frontend available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${frontend_port}"
EOF

chmod +x deploy.sh

# Set up log rotation
cat > /etc/logrotate.d/qr-generator << 'EOF'
/opt/qr-generator/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 ec2-user ec2-user
}
EOF

echo "QR Generator infrastructure setup completed!"
