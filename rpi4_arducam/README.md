# Arducam Mini 2MP Plus (OV2640) for Raspberry Pi 4

Python library and capture scripts for using the **Arducam Mini 2MP Plus - OV2640 SPI Camera Module** with **Raspberry Pi 4**.

This is adapted from the original Raspberry Pi Pico code to work with standard Python on Raspberry Pi 4.

## Hardware Requirements

- Raspberry Pi 4 (or other Raspberry Pi with 40-pin header)
- Arducam Mini 2MP Plus (OV2640) SPI Camera Module
- Jumper wires for connections

## Wiring Connections

Connect the Arducam to your Raspberry Pi 4 as follows:

| Arducam Pin | Raspberry Pi 4 Pin | Description |
|-------------|-------------------|-------------|
| CS          | GPIO 17 (Pin 11)  | SPI Chip Select |
| MOSI        | GPIO 10 (Pin 19)  | SPI MOSI |
| MISO        | GPIO 9 (Pin 21)   | SPI MISO |
| SCK         | GPIO 11 (Pin 23)  | SPI Clock |
| GND         | GND (Pin 6, 9, etc) | Ground |
| VCC         | 3.3V (Pin 1, 17)  | Power (3.3V) |
| SDA         | GPIO 2 (Pin 3)    | I2C Data |
| SCL         | GPIO 3 (Pin 5)    | I2C Clock |

**Important Notes:**
- Use **3.3V power** only (DO NOT use 5V)
- Default CS pin is GPIO 17 (BCM numbering)
- SPI and I2C must be enabled on your Raspberry Pi

## Installation

### 1. Enable SPI and I2C

Run the Raspberry Pi configuration tool:

```bash
sudo raspi-config
```

Navigate to:
- **Interface Options** → **SPI** → Enable
- **Interface Options** → **I2C** → Enable

Reboot your Raspberry Pi:

```bash
sudo reboot
```

### 2. Install Python Dependencies

```bash
# Update package list
sudo apt-get update

# Install system dependencies
sudo apt-get install -y python3-pip python3-dev

# Navigate to the project directory
cd rpi4_arducam

# Install Python packages
pip3 install -r requirements.txt
```

### 3. Verify Installation

Test that SPI and I2C are enabled:

```bash
# Check SPI
ls /dev/spi*
# Should show: /dev/spidev0.0  /dev/spidev0.1

# Check I2C
ls /dev/i2c*
# Should show: /dev/i2c-1
```

## Usage

### Video Recording (NEW!)

Record a 10-second video at 10 FPS:

```bash
python3 record_video.py
```

Record custom duration and frame rate:

```bash
# 30 second video at 15 FPS
python3 record_video.py -d 30 --fps 15

# Lower resolution for higher frame rate
python3 record_video.py -r 320x240 --fps 20

# Custom output filename
python3 record_video.py -o myvideo.mp4

# Keep individual frame files
python3 record_video.py --keep-frames
```

**Requirements**: Install ffmpeg first:
```bash
sudo apt-get install ffmpeg
```

**Note**: Video recording captures individual JPEG frames and compiles them with ffmpeg. Realistic frame rates:
- 320×240: 15-20 FPS
- 640×480: 8-12 FPS
- 800×600: 5-8 FPS

### Time-Lapse Recording

For time-lapse photography (no ffmpeg required):

```bash
# 60 seconds, one frame per second
python3 record_timelapse.py -d 60 -i 1

# 10 minutes, frame every 5 seconds
python3 record_timelapse.py -d 600 -i 5

# 1 hour, frame every 30 seconds at max resolution
python3 record_timelapse.py -d 3600 -i 30 -r 1600x1200
```

Convert frames to video afterward:
```bash
ffmpeg -framerate 30 -i timelapse_*/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p video.mp4
```

### Simple Image Capture

Capture a single image with default settings (640x480):

```bash
python3 capture_image.py
```

Capture with custom resolution and filename:

```bash
# Available resolutions: 0-8
# 0=160x120, 1=176x144, 2=320x240, 3=352x288, 4=640x480 (default)
# 5=800x600, 6=1024x768, 7=1280x1024, 8=1600x1200

python3 capture_image.py -o myimage.jpg -r 8
```

### Advanced Capture with Effects

The advanced script supports various image effects and settings:

```bash
# Capture at 1600x1200 resolution
python3 capture_advanced.py -r 1600x1200 -o photo.jpg

# Capture with sepia effect and office lighting
python3 capture_advanced.py -e sepia -l office

# Capture with black and white effect
python3 capture_advanced.py -e bw

# Adjust brightness and contrast
python3 capture_advanced.py --brightness 1 --contrast -1

# Capture 10 images at 2-second intervals
python3 capture_advanced.py --continuous 10 --interval 2

# Time-lapse: 60 images at 5-second intervals
python3 capture_advanced.py --continuous 60 --interval 5 --prefix timelapse
```

### Available Options

**Resolutions:**
- `160x120`, `176x144`, `320x240`, `352x288`, `640x480` (default)
- `800x600`, `1024x768`, `1280x1024`, `1600x1200`

**Light Modes:**
- `auto` (default), `sunny`, `cloudy`, `office`, `home`

**Special Effects:**
- `normal` (default), `antique`, `bluish`, `greenish`, `reddish`
- `bw` (black & white), `negative`, `sepia`

**Adjustments:**
- `--brightness`: -2 to 2 (0 is default)
- `--contrast`: -2 to 2 (0 is default)
- `--saturation`: -2 to 2 (0 is default)

## Python API

You can also use the library in your own Python scripts:

```python
from Arducam_RPI4 import ArducamClass, OV2640, OV2640_640x480
import time

# Initialize camera
camera = ArducamClass(OV2640)

# Detect and initialize
camera.Camera_Detection()
camera.Spi_Test()
camera.Camera_Init()
time.sleep(1)

# Configure camera
camera.OV2640_set_JPEG_size(OV2640_640x480)
camera.clear_fifo_flag()

# Capture image
camera.flush_fifo()
camera.clear_fifo_flag()
camera.start_capture()

# Wait for capture to complete
while camera.get_bit(0x41, 0x08) == 0:
    time.sleep(0.01)

# Read and save image
image_data = camera.read_fifo_burst()
with open('image.jpg', 'wb') as f:
    f.write(image_data)

# Cleanup
del camera
```

## Troubleshooting

### Camera Not Detected

1. **Check wiring connections** - Ensure all pins are properly connected
2. **Verify I2C is enabled** - Run `ls /dev/i2c*` to confirm
3. **Check I2C devices** - Run `sudo i2cdetect -y 1` to see if camera is detected at address 0x30
4. **Check power** - Ensure you're using 3.3V (NOT 5V)

### SPI Interface Error

1. **Verify SPI is enabled** - Run `ls /dev/spi*` to confirm
2. **Check wiring** - Verify MOSI, MISO, SCK, and CS connections
3. **Check CS pin** - Default is GPIO 17, make sure it matches your wiring

### Image Capture Timeout

1. **Increase timeout** - Edit the script to increase timeout duration
2. **Check camera initialization** - Ensure all initialization steps complete successfully
3. **Try lower resolution** - Start with 320x240 to test

### Permission Errors

If you get permission errors accessing SPI or I2C:

```bash
# Add your user to the necessary groups
sudo usermod -a -G spi,i2c,gpio $USER

# Log out and back in for changes to take effect
```

### Module Import Errors

If you get "No module named 'spidev'" or similar:

```bash
# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# Or install individually
pip3 install spidev smbus2 RPi.GPIO
```

## Customization

### Using Different Pins

To use different GPIO pins for CS (chip select):

```python
from Arducam_RPI4 import ArducamClass, OV2640

# Use GPIO 27 for CS instead of default GPIO 17
camera = ArducamClass(OV2640, cs_pin=27)
```

## File Structure

```
rpi4_arducam/
├── Arducam_RPI4.py          # Main camera library
├── OV2640_reg.py            # OV2640 register definitions
├── capture_image.py         # Simple capture script
├── capture_advanced.py      # Advanced capture with effects
├── record_video.py          # Video recording (requires ffmpeg)
├── record_timelapse.py      # Time-lapse recording
├── test_camera.py           # Diagnostic and testing tool
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── WIRING.md               # Wiring diagrams
└── TROUBLESHOOTING_JPEG.md # JPEG error troubleshooting
```

## References

- [Arducam Product Page](https://www.arducam.com/)
- [OV2640 Datasheet](https://www.ovt.com/products/ov2640/)
- [Raspberry Pi SPI Documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/)
- [Raspberry Pi I2C Documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/i2c/)

## License

This code is adapted from the original Arducam PICO_SPI_CAM examples and modified for Raspberry Pi 4.

## Support

For issues and questions:
1. Check the Troubleshooting section above
2. Verify all hardware connections
3. Ensure SPI and I2C are properly enabled
4. Check the original repository for updates

## Changelog

### Version 1.0 (2025-11-25)
- Initial release
- Adapted from Raspberry Pi Pico code to Raspberry Pi 4
- Support for OV2640 camera module
- Simple and advanced capture scripts
- Full support for resolutions, effects, and adjustments

