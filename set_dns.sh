#!/bin/bash

# Create a backup of the original resolv.conf
sudo cp /etc/resolv.conf /etc/resolv.conf.bak

# Update /etc/resolv.conf with the custom DNS settings
echo "nameserver 127.0.0.53" | sudo tee /etc/resolv.conf
echo "options edns0 trust-ad" | sudo tee -a /etc/resolv.conf
echo "search qjd1uhw1tstuviscw2qx4dak1c.dx.internal.cloudapp.net" | sudo tee -a /etc/resolv.conf

# Inform the user
echo "DNS settings updated successfully."
