#!/bin/bash

echo "======================================"
echo " Offline AI Hands-Free Book Reader"
echo " Setup Script (Linux)"
echo "======================================"

# Stop on error
set -e

# Update system
echo "[1/6] Updating system..."
sudo apt update

# Install system dependencies
echo "[2/6] Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    tesseract-ocr \
    portaudio19-dev \
    espeak \
    libreoffice

# Upgrade pip
echo "[3/6] Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Python requirements
echo "[4/6] Installing Python packages..."
pip3 install -r requirements.txt

# Download NLTK data
echo "[5/6] Downloading NLTK tokenizer..."
python3 - <<EOF
import nltk
nltk.download('punkt')
EOF

# Finish
echo "[6/6] Setup completed successfully!"
echo ""
echo "To run the application:"
echo "   python3 app.py"
echo ""
