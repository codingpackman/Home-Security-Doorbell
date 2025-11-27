# Quick Start Guide

Get your Arducam OV2640 working on Raspberry Pi 4 in under 10 minutes!

## Step 1: Wire the Camera (5 min)

Connect your Arducam to Raspberry Pi 4:

| Arducam | → | Raspberry Pi 4 |
|---------|---|----------------|
| VCC     | → | Pin 1 (3.3V)   |
| GND     | → | Pin 6 (GND)    |
| CS      | → | Pin 11 (GPIO 17) |
| MOSI    | → | Pin 19 (GPIO 10) |
| MISO    | → | Pin 21 (GPIO 9)  |
| SCK     | → | Pin 23 (GPIO 11) |
| SDA     | → | Pin 3 (GPIO 2)   |
| SCL     | → | Pin 5 (GPIO 3)   |

⚠️ **Important**: Use 3.3V, NOT 5V!

See [WIRING.md](WIRING.md) for detailed pinout diagrams.

## Step 2: Enable SPI and I2C (2 min)

```bash
# Open configuration tool
sudo raspi-config

# Navigate to: Interface Options → SPI → Enable
# Navigate to: Interface Options → I2C → Enable
# Select Finish and reboot

sudo reboot
```

## Step 3: Install Software (2 min)

```bash
# Navigate to the project folder
cd ~/rpi4_arducam

# Install dependencies
pip3 install -r requirements.txt
```

## Step 4: Test the Camera (1 min)

```bash
# Capture your first image!
python3 capture_image.py
```

If successful, you'll see:
```
Initializing camera...
Detecting camera...
Camera detected: OV2640
Testing SPI interface...
SPI interface OK
...
Image saved: capture_20251125_143022.jpg
✓ Success!
```

## Common Issues

### "Cannot find OV2640 module"
- Check all wire connections
- Verify I2C is enabled: `ls /dev/i2c*`
- Run: `sudo i2cdetect -y 1` to check if device appears at 0x30

### "SPI interface Error"
- Verify SPI is enabled: `ls /dev/spi*`
- Check CS, MOSI, MISO, SCK connections
- Ensure CS is on GPIO 17 (Pin 11)

### Permission Denied
```bash
sudo usermod -a -G spi,i2c,gpio $USER
# Log out and back in
```

## Next Steps

### Try Different Resolutions
```bash
# High resolution (1600x1200)
python3 capture_image.py -r 8 -o highres.jpg

# Small thumbnail (160x120)
python3 capture_image.py -r 0 -o thumbnail.jpg
```

### Apply Effects
```bash
# Black and white
python3 capture_advanced.py -e bw

# Sepia tone
python3 capture_advanced.py -e sepia

# Negative
python3 capture_advanced.py -e negative
```

### Time-Lapse Photography
```bash
# Capture 60 images, one every 5 seconds
python3 capture_advanced.py --continuous 60 --interval 5 --prefix timelapse
```

### Adjust Image Quality
```bash
# Increase brightness and contrast
python3 capture_advanced.py --brightness 2 --contrast 1

# Sunny day outdoor shot
python3 capture_advanced.py -l sunny --saturation 1
```

## Usage Examples

### Basic capture (default 640x480)
```bash
python3 capture_image.py
```

### High-res capture with custom name
```bash
python3 capture_image.py -r 8 -o myimage.jpg
```

### Capture with effects
```bash
python3 capture_advanced.py -r 1600x1200 -e sepia -l office
```

### Time-lapse (100 images at 10-second intervals)
```bash
python3 capture_advanced.py --continuous 100 --interval 10
```

## Need Help?

1. Check [README.md](README.md) for full documentation
2. See [WIRING.md](WIRING.md) for connection diagrams
3. Review the Troubleshooting section in README.md

## Resolution Reference

| Code | Resolution | Use Case |
|------|------------|----------|
| 0 | 160x120 | Tiny thumbnail |
| 1 | 176x144 | Small thumbnail |
| 2 | 320x240 | Low res preview |
| 3 | 352x288 | Small preview |
| 4 | 640x480 | Standard (default) |
| 5 | 800x600 | Good quality |
| 6 | 1024x768 | High quality |
| 7 | 1280x1024 | Very high quality |
| 8 | 1600x1200 | Maximum quality |

Enjoy your camera! 📷

