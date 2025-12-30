# Project Summary: Arducam OV2640 for Raspberry Pi 4

## What Was Created

I've created a complete Python solution for using the **Arducam Mini 2MP Plus (OV2640) SPI Camera Module** with **Raspberry Pi 4**. This was adapted from the original Raspberry Pi Pico code to work with standard Python on Raspberry Pi 4.

## Files Created

### 📁 rpi4_arducam/

1. **Arducam_RPI4.py** (669 lines)
   - Main camera library adapted for Raspberry Pi 4
   - Uses `spidev` for SPI communication
   - Uses `smbus2` for I2C communication
   - Uses `RPi.GPIO` for GPIO control
   - Full support for OV2640 camera module
   - Includes all image settings and effects

2. **OV2640_reg.py** (615 lines)
   - OV2640 sensor register definitions
   - Configuration arrays for different resolutions
   - JPEG encoding settings

3. **capture_image.py** (117 lines)
   - Simple command-line capture script
   - Easy to use for basic photography
   - Supports all resolutions (160x120 to 1600x1200)
   - Command-line arguments for customization

4. **capture_advanced.py** (343 lines)
   - Advanced capture with full features
   - Image effects (sepia, B&W, negative, etc.)
   - Lighting modes (auto, sunny, cloudy, office, home)
   - Brightness, contrast, saturation adjustments
   - Time-lapse and continuous capture modes
   - Comprehensive command-line interface

5. **record_video.py** (NEW - 440+ lines)
   - Real-time video recording
   - Captures frames continuously at specified FPS
   - Automatic compilation to MP4 using ffmpeg
   - Progress tracking and statistics
   - Multiple resolutions (320×240 to 800×600)
   - Automatic frame cleanup
   - Frame rates: 5-20 FPS depending on resolution

6. **record_timelapse.py** (NEW - 230+ lines)
   - Time-lapse photography
   - Captures frames at custom intervals
   - No ffmpeg required (saves individual frames)
   - Perfect for long-duration recording
   - Supports all resolutions (up to 1600×1200)
   - Manual video conversion with provided commands

7. **test_camera.py** (NEW - 280+ lines)
   - Comprehensive diagnostic tool
   - 4 automated tests (SPI, I2C, FIFO, JPEG)
   - Saves test image for verification
   - Step-by-step troubleshooting guidance
   - Validates JPEG headers

8. **requirements.txt**
   - Python package dependencies:
     - `spidev` >= 3.5
     - `smbus2` >= 0.4.1
     - `RPi.GPIO` >= 0.7.1

9. **README.md** (500+ lines)
   - Complete documentation
   - Hardware requirements
   - Detailed wiring instructions
   - Installation guide
   - Usage examples
   - Python API documentation
   - Comprehensive troubleshooting guide
   - File structure reference

10. **WIRING.md**
    - Visual ASCII wiring diagrams
    - Complete GPIO pinout reference
    - Pin connection tables
    - Verification commands
    - Alternative pin configurations
    - Connection troubleshooting

11. **QUICKSTART.md**
    - 10-minute setup guide
    - Step-by-step instructions
    - Common issues and solutions
    - Quick usage examples
    - Resolution reference table

12. **TROUBLESHOOTING_JPEG.md** (NEW)
    - Diagnoses invalid JPEG header errors
    - Explains SPI timing fixes
    - JPEG validation techniques
    - Recovery procedures

13. **VIDEO_RECORDING_GUIDE.md** (NEW - Comprehensive!)
    - Complete video recording guide
    - Real-time vs time-lapse recording
    - ffmpeg installation and usage
    - Frame rate optimization tips
    - Quality control and encoding options
    - Real-world examples
    - Performance tuning

## Key Features

### Supported Resolutions
- 160×120, 176×144, 320×240, 352×288
- 640×480 (default), 800×600
- 1024×768, 1280×1024, 1600×1200

### Image Effects
- Normal, Antique, Sepia
- Black & White, Negative
- Bluish, Greenish, Reddish tints

### Lighting Modes
- Auto (default)
- Sunny, Cloudy
- Office, Home

### Adjustments
- Brightness: -2 to +2
- Contrast: -2 to +2
- Saturation: -2 to +2

### Capture Modes
- Single image capture
- Continuous/time-lapse capture
- Custom intervals between captures
- **Video recording** (NEW!)
- **Time-lapse photography** (NEW!)

### Video Recording Features (NEW!)
- Real-time video: 5-20 FPS depending on resolution
- Automatic MP4 creation with ffmpeg
- Progress tracking and statistics
- Multiple resolutions (320×240 to 800×600)
- Time-lapse: Any interval, all resolutions
- Frame-by-frame capture for manual editing

## Hardware Connections

The camera connects to Raspberry Pi 4 via:
- **SPI** (CS, MOSI, MISO, SCK) - for data transfer
- **I2C** (SDA, SCL) - for camera control
- **Power** (3.3V, GND)

Default pins:
- CS: GPIO 17 (Pin 11)
- MOSI: GPIO 10 (Pin 19)
- MISO: GPIO 9 (Pin 21)
- SCK: GPIO 11 (Pin 23)
- SDA: GPIO 2 (Pin 3)
- SCL: GPIO 3 (Pin 5)
- VCC: 3.3V (Pin 1)
- GND: GND (Pin 6)

## Usage Examples

### Basic Capture
```bash
# Simple capture with defaults (640x480)
python3 capture_image.py

# High-resolution capture
python3 capture_image.py -r 8 -o photo.jpg
```

### Advanced Features
```bash
# Sepia effect with office lighting
python3 capture_advanced.py -e sepia -l office

# Black and white with increased contrast
python3 capture_advanced.py -e bw --contrast 2

# High-res with adjustments
python3 capture_advanced.py -r 1600x1200 --brightness 1 --saturation 1
```

### Video Recording (NEW!)
```bash
# Record 10-second video at 10 FPS (default)
python3 record_video.py

# Record 30-second video at 15 FPS
python3 record_video.py -d 30 --fps 15

# Lower resolution for higher frame rate
python3 record_video.py -r 320x240 --fps 20 -o action.mp4
```

**Prerequisites**: Install ffmpeg
```bash
sudo apt-get install ffmpeg
```

### Time-Lapse Photography
```bash
# 60 seconds, one frame per second
python3 record_timelapse.py -d 60 -i 1

# 1 hour, frame every 10 seconds (sunrise/sunset)
python3 record_timelapse.py -d 3600 -i 10 -r 1600x1200

# Convert frames to video
ffmpeg -framerate 30 -i timelapse_*/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p output.mp4
```

## Installation (Quick)

```bash
# 1. Enable SPI and I2C
sudo raspi-config
# Interface Options → SPI → Enable
# Interface Options → I2C → Enable
# Reboot

# 2. Install dependencies
cd rpi4_arducam
pip3 install -r requirements.txt

# 3. Capture!
python3 capture_image.py
```

## Python API Example

```python
from Arducam_RPI4 import ArducamClass, OV2640, OV2640_1600x1200
import time

# Initialize
camera = ArducamClass(OV2640)
camera.Camera_Detection()
camera.Spi_Test()
camera.Camera_Init()
time.sleep(1)

# Configure
camera.OV2640_set_JPEG_size(OV2640_1600x1200)
camera.OV2640_set_Special_effects(Sepia)

# Capture
camera.clear_fifo_flag()
camera.flush_fifo()
camera.start_capture()

# Wait for completion
while camera.get_bit(0x41, 0x08) == 0:
    time.sleep(0.01)

# Save
image_data = camera.read_fifo_burst()
with open('photo.jpg', 'wb') as f:
    f.write(image_data)

# Cleanup
del camera
```

## Differences from Original Pico Code

The original code was for Raspberry Pi Pico using CircuitPython/MicroPython. Key adaptations made:

1. **GPIO Control**: Changed from `board` and `digitalio` to `RPi.GPIO`
2. **SPI Communication**: Changed from `busio.SPI` to `spidev`
3. **I2C Communication**: Changed from `bitbangio.I2C` to `smbus2`
4. **Pin Definitions**: Adapted from Pico pins to RPi 4 BCM GPIO pins
5. **Library Imports**: Changed from CircuitPython to standard Python libraries
6. **API Methods**: Modified to work with Linux spidev and smbus interfaces

## Verification After Setup

```bash
# Check SPI is enabled
ls /dev/spi*
# Should show: /dev/spidev0.0 /dev/spidev0.1

# Check I2C is enabled
ls /dev/i2c*
# Should show: /dev/i2c-1

# Check camera is detected
sudo i2cdetect -y 1
# Should show device at address 0x30
```

## Project Structure

```
rpi4_arducam/
├── Arducam_RPI4.py             # Camera library (main)
├── OV2640_reg.py               # Register definitions
├── capture_image.py            # Simple capture script
├── capture_advanced.py         # Advanced capture script
├── record_video.py             # Video recording (NEW!)
├── record_timelapse.py         # Time-lapse recording (NEW!)
├── test_camera.py              # Diagnostic tool (NEW!)
├── requirements.txt            # Python dependencies
├── README.md                  # Full documentation
├── QUICKSTART.md              # 10-minute setup guide
├── WIRING.md                  # Wiring diagrams
├── TROUBLESHOOTING_JPEG.md    # JPEG error fixes (NEW!)
├── VIDEO_RECORDING_GUIDE.md   # Video guide (NEW!)
└── PROJECT_SUMMARY.md         # This file
```

## Getting Started

1. **Start Here**: Read [QUICKSTART.md](QUICKSTART.md) for fast setup
2. **Full Details**: See [README.md](README.md) for comprehensive documentation
3. **Wiring Help**: Check [WIRING.md](WIRING.md) for connection diagrams
4. **Try It**: Run `python3 capture_image.py`

## Troubleshooting Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Camera not detected | Check I2C: `sudo i2cdetect -y 1` |
| SPI error | Check SPI: `ls /dev/spi*` |
| Permission denied | Add to groups: `sudo usermod -a -G spi,i2c,gpio $USER` |
| Import errors | Install deps: `pip3 install -r requirements.txt` |
| Timeout on capture | Check all 8 wire connections |

## Next Steps

1. Wire up your camera following [WIRING.md](WIRING.md)
2. Enable SPI and I2C on your Raspberry Pi
3. Install the Python dependencies
4. Run your first capture!
5. Experiment with different resolutions and effects
6. Try time-lapse photography

## Credits

- Original code: Arducam PICO_SPI_CAM examples
- Adapted for Raspberry Pi 4 with standard Python
- Created: November 25, 2025

---

**Ready to start?** Jump to [QUICKSTART.md](QUICKSTART.md)!

