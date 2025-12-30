#!/bin/bash
# Smart Doorbell System - Raspberry Pi Setup Script
# This script automates the setup process on Raspberry Pi 4

echo "=========================================="
echo "Smart Doorbell System Setup"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "This script will:"
echo "  1. Update system packages"
echo "  2. Install ffmpeg"
echo "  3. Install AWS CLI"
echo "  4. Install Python dependencies"
echo "  5. Create recordings directory"
echo "  6. Enable SPI interface"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

echo ""
echo "=========================================="
echo "Step 1: Updating System Packages"
echo "=========================================="
sudo apt-get update
if [ $? -ne 0 ]; then
    echo "❌ Failed to update packages"
    exit 1
fi
echo "✅ System packages updated"

echo ""
echo "=========================================="
echo "Step 2: Installing ffmpeg"
echo "=========================================="
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg already installed"
else
    sudo apt-get install -y ffmpeg
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install ffmpeg"
        exit 1
    fi
    echo "✅ ffmpeg installed"
fi

echo ""
echo "=========================================="
echo "Step 3: Installing AWS CLI"
echo "=========================================="
if command -v aws &> /dev/null; then
    echo "✅ AWS CLI already installed"
else
    sudo apt-get install -y awscli
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install AWS CLI"
        exit 1
    fi
    echo "✅ AWS CLI installed"
fi

echo ""
echo "=========================================="
echo "Step 4: Installing Python Dependencies"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAIN_DIR="$SCRIPT_DIR"
ARDUCAM_DIR="$(dirname "$SCRIPT_DIR")/rpi4_arducam"

# Install main requirements
if [ -f "$MAIN_DIR/requirements.txt" ]; then
    echo "Installing main system dependencies..."
    pip3 install -r "$MAIN_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install main dependencies"
        exit 1
    fi
    echo "✅ Main dependencies installed"
else
    echo "❌ requirements.txt not found in main directory"
    exit 1
fi

# Install arducam requirements
if [ -f "$ARDUCAM_DIR/requirements.txt" ]; then
    echo "Installing Arducam dependencies..."
    pip3 install -r "$ARDUCAM_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Arducam dependencies"
        exit 1
    fi
    echo "✅ Arducam dependencies installed"
else
    echo "⚠️  Warning: Arducam requirements.txt not found"
fi

echo ""
echo "=========================================="
echo "Step 5: Creating Recordings Directory"
echo "=========================================="
RECORDINGS_DIR="$MAIN_DIR/recordings"
if [ ! -d "$RECORDINGS_DIR" ]; then
    mkdir -p "$RECORDINGS_DIR"
    echo "✅ Created recordings directory: $RECORDINGS_DIR"
else
    echo "✅ Recordings directory already exists"
fi

echo ""
echo "=========================================="
echo "Step 6: Enabling SPI Interface"
echo "=========================================="
if grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "✅ SPI already enabled"
else
    echo "Enabling SPI interface..."
    sudo raspi-config nonint do_spi 0
    if [ $? -ne 0 ]; then
        echo "⚠️  Warning: Failed to enable SPI automatically"
        echo "   Please enable SPI manually:"
        echo "   sudo raspi-config"
        echo "   Interface Options > SPI > Enable"
    else
        echo "✅ SPI enabled"
        NEED_REBOOT=true
    fi
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure AWS credentials:"
echo "   $ aws configure"
echo "   (Enter your AWS Access Key ID and Secret Access Key)"
echo ""
echo "2. Verify MongoDB connection string in main_system.py"
echo ""
echo "3. Test the camera:"
echo "   $ cd $ARDUCAM_DIR"
echo "   $ python3 test_camera.py"
echo ""
echo "4. Test the system:"
echo "   $ cd $MAIN_DIR"
echo "   $ python3 test_doorbell.py button"
echo ""
echo "5. Run the full system:"
echo "   $ python3 main_system.py"
echo ""

if [ "$NEED_REBOOT" = true ]; then
    echo "⚠️  IMPORTANT: System reboot required for SPI changes"
    echo ""
    read -p "Reboot now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Rebooting..."
        sudo reboot
    else
        echo "Please reboot manually before using the camera:"
        echo "$ sudo reboot"
    fi
fi

echo ""
echo "For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "For quick reference, see QUICK_REFERENCE.md"
echo ""

