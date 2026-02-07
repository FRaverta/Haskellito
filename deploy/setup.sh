#!/bin/bash
set -e

# Haskellito Server Setup Script for Ubuntu 22.04 (AWS Lightsail)
# Run as root or with sudo

echo "=== Haskellito Server Setup ==="

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python 3.11
echo "Installing Python 3.11..."
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install GHC (Haskell compiler with GHCi)
echo "Installing GHC..."
apt-get install -y ghc

# Install Node.js 20.x for frontend build
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Nginx
echo "Installing Nginx..."
apt-get install -y nginx

# Create application directory
echo "Setting up application directory..."
mkdir -p /opt/haskellito
mkdir -p /var/www/haskellito

# Create application user
if ! id -u haskellito > /dev/null 2>&1; then
    useradd -r -s /bin/false haskellito
fi

# Set ownership
chown -R haskellito:haskellito /opt/haskellito

# Install Python dependencies globally or in venv
echo "Setting up Python virtual environment..."
cd /opt/haskellito
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# Copy systemd service file
echo "Installing systemd service..."
cp /opt/haskellito/deploy/haskellito.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable haskellito

# Copy nginx configuration
echo "Configuring Nginx..."
cp /opt/haskellito/deploy/nginx.conf /etc/nginx/sites-available/haskellito
ln -sf /etc/nginx/sites-available/haskellito /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

# Restart nginx
systemctl restart nginx
systemctl enable nginx

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Clone your repo to /opt/haskellito"
echo "2. Run: cd /opt/haskellito && source venv/bin/activate && pip install -r requirements.txt"
echo "3. Build frontend: cd frontend && npm install && npm run build"
echo "4. Copy frontend build: cp -r frontend/dist/* /var/www/haskellito/"
echo "5. Start the service: sudo systemctl start haskellito"
echo "6. Check status: sudo systemctl status haskellito"
echo ""
echo "Optional: Install SSL with Let's Encrypt:"
echo "  sudo apt install certbot python3-certbot-nginx"
echo "  sudo certbot --nginx -d yourdomain.com"
