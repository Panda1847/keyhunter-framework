#!/bin/bash

# Hybrid Web Scraper/Crawler Installer for Kali Linux

echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install curl_cffi nodriver aiohttp loguru requests

echo "Installation complete. To run the scraper, use:"
echo "source venv/bin/activate"
echo "python3 main.py --urls <url1> <url2> ..."
