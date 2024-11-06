#!/bin/bash

# Set a custom DNS to match GitHub Actions runner's configuration
echo -e "nameserver 127.0.0.53\noptions edns0 trust-ad\nsearch rca3p110zaveja4ulz44at14fe.dx.internal.cloudapp.net" | sudo tee /etc/resolv.conf > /dev/null

# Set a new hostname (customize as needed)
NEW_HOSTNAME="custom-codespace-server"
echo $NEW_HOSTNAME | sudo tee /etc/hostname > /dev/null
sudo hostname $NEW_HOSTNAME

# Update /etc/hosts to reflect the new hostname for loopback
sudo sed -i "s/127.0.0.1 .*/127.0.0.1 $NEW_HOSTNAME localhost/" /etc/hosts

# Run system updates (optional but useful for a fresh environment)
sudo apt-get update && sudo apt-get upgrade -y
