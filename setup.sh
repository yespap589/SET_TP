#!/bin/bash

# Update package list and upgrade existing packages
echo "Updating and upgrading packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3.12.7
echo "Installing Python 3.12.7..."
sudo apt-get install -y python3.12

# Install pip for Python 3.12
echo "Installing pip for Python 3.12..."
sudo apt-get install -y python3.12-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# Verify installation
echo "Verifying Python installation..."
python3.12 --version

echo "Setup complete!"
