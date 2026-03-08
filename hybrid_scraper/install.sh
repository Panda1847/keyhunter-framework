#!/bin/bash

# KeyHunter Framework Installer for Kali Linux
# Optimized for professional cybersecurity research environments

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[*] Initializing KeyHunter Framework Installation...${NC}"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Please run as root or with sudo${NC}"
  exit 1
fi

echo -e "${BLUE}[*] Updating system package lists...${NC}"
apt update -y

echo -e "${BLUE}[*] Installing system dependencies...${NC}"
apt install -y python3-pip python3-venv git curl libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2

# Setup working directory
INSTALL_DIR=$(pwd)
echo -e "${BLUE}[*] Setting up Python virtual environment in ${INSTALL_DIR}/venv...${NC}"

if [ -d "venv" ]; then
    echo -e "${BLUE}[*] Existing venv found. Refreshing...${NC}"
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

echo -e "${BLUE}[*] Installing Python requirements...${NC}"
pip install --upgrade pip
pip install curl_cffi nodriver aiohttp loguru requests

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${BLUE}[*] To start the framework:${NC}"
echo -e "    source venv/bin/activate"
echo -e "    python3 main.py --urls <url1> <url2> ..."
echo -e ""
echo -e "${BLUE}[*] Example:${NC}"
echo -e "    python3 main.py --urls https://example.com --dynamic"
