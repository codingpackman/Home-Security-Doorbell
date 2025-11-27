# Wiring Diagram for Arducam OV2640 to Raspberry Pi 4

## Pin Connections

```
Arducam OV2640          Raspberry Pi 4
┌──────────────┐        ┌──────────────────┐
│              │        │                  │
│     CS   ────┼────────┼──► GPIO 17 (11) │  SPI Chip Select
│              │        │                  │
│    MOSI  ────┼────────┼──► GPIO 10 (19) │  SPI MOSI (Master Out Slave In)
│              │        │                  │
│    MISO  ────┼────────┼──► GPIO 9  (21) │  SPI MISO (Master In Slave Out)
│              │        │                  │
│    SCK   ────┼────────┼──► GPIO 11 (23) │  SPI Clock
│              │        │                  │
│    GND   ────┼────────┼──► GND     (6)  │  Ground
│              │        │                  │
│    VCC   ────┼────────┼──► 3.3V    (1)  │  Power ⚠️ 3.3V ONLY!
│              │        │                  │
│    SDA   ────┼────────┼──► GPIO 2  (3)  │  I2C Data
│              │        │                  │
│    SCL   ────┼────────┼──► GPIO 3  (5)  │  I2C Clock
│              │        │                  │
└──────────────┘        └──────────────────┘
```

## Raspberry Pi 4 GPIO Pinout Reference

```
          3.3V (1)  ● ● (2)  5V
    GPIO 2 SDA (3)  ● ● (4)  5V
    GPIO 3 SCL (5)  ● ● (6)  GND
        GPIO 4 (7)  ● ● (8)  GPIO 14
           GND (9)  ● ● (10) GPIO 15
   GPIO 17 CS (11)  ● ● (12) GPIO 18
       GPIO 27 (13) ● ● (14) GND
       GPIO 22 (15) ● ● (16) GPIO 23
          3.3V (17) ● ● (18) GPIO 24
 GPIO 10 MOSI (19)  ● ● (20) GND
  GPIO 9 MISO (21)  ● ● (22) GPIO 25
 GPIO 11 SCLK (23)  ● ● (24) GPIO 8
           GND (25) ● ● (26) GPIO 7
       GPIO 0  (27) ● ● (28) GPIO 1
       GPIO 5  (29) ● ● (30) GND
       GPIO 6  (31) ● ● (32) GPIO 12
       GPIO 13 (33) ● ● (34) GND
       GPIO 19 (35) ● ● (36) GPIO 16
       GPIO 26 (37) ● ● (38) GPIO 20
           GND (39) ● ● (40) GPIO 21

Legend:
● Marked pins are used by Arducam
```

## Quick Reference Table

| Function    | Arducam Pin | Pi GPIO | Pi Physical Pin |
|-------------|-------------|---------|-----------------|
| Power       | VCC         | 3.3V    | Pin 1 or 17     |
| Ground      | GND         | GND     | Pin 6, 9, 14... |
| SPI CS      | CS          | GPIO 17 | Pin 11          |
| SPI MOSI    | MOSI        | GPIO 10 | Pin 19          |
| SPI MISO    | MISO        | GPIO 9  | Pin 21          |
| SPI Clock   | SCK         | GPIO 11 | Pin 23          |
| I2C Data    | SDA         | GPIO 2  | Pin 3           |
| I2C Clock   | SCL         | GPIO 3  | Pin 5           |

## Important Warnings

⚠️ **POWER**: Use 3.3V ONLY! Do NOT connect to 5V or you will damage the camera!

⚠️ **STATIC**: Handle the camera module carefully to avoid static damage

⚠️ **CONNECTIONS**: Ensure all connections are secure before powering on

## Pin Numbering

This project uses **BCM (Broadcom) pin numbering**, not physical pin numbers.

- BCM numbering refers to GPIO numbers (e.g., GPIO 17)
- Physical numbering refers to pin position on the header (e.g., Pin 11)

The code uses BCM numbering (GPIO.BCM mode).

## Verification Commands

After wiring, verify connections with these commands:

### Check SPI is detected:
```bash
ls /dev/spi*
# Should show: /dev/spidev0.0  /dev/spidev0.1
```

### Check I2C is detected:
```bash
ls /dev/i2c*
# Should show: /dev/i2c-1
```

### Scan for I2C devices:
```bash
sudo i2cdetect -y 1
# Should show device at address 0x30 (OV2640)
```

### Expected output from i2cdetect:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: 30 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
```

## Alternative CS Pin

If GPIO 17 is already in use, you can use a different pin for CS. Modify your code:

```python
from Arducam_RPI4 import ArducamClass, OV2640

# Use GPIO 27 instead of default GPIO 17
camera = ArducamClass(OV2640, cs_pin=27)
```

Common alternative CS pins: GPIO 8, GPIO 7, GPIO 27

## Troubleshooting Connections

### Camera not detected?
1. Check all 8 pins are connected
2. Verify power is 3.3V (measure with multimeter if available)
3. Check for loose connections
4. Try reseating all connections

### I2C device not showing at 0x30?
1. Verify SDA and SCL connections
2. Check I2C is enabled: `sudo raspi-config` → Interface Options → I2C
3. Check pull-up resistors (usually built-in on Pi)
4. Try: `sudo i2cdetect -y 1` to scan bus

### SPI errors?
1. Verify MOSI, MISO, SCK, and CS connections
2. Check SPI is enabled: `sudo raspi-config` → Interface Options → SPI
3. Ensure no other devices are using the same CS pin

