"""
Arducam Library for Raspberry Pi 4
Adapted from Pico version to work with standard Python on Raspberry Pi 4
"""

import spidev
import smbus2
import time
import RPi.GPIO as GPIO
from OV2640_reg import *

# Camera Types
OV2640 = 0
OV5642 = 1

# Constants
MAX_FIFO_SIZE = 0x7FFFFF
ARDUCHIP_FRAMES = 0x01
ARDUCHIP_TIM = 0x03
VSYNC_LEVEL_MASK = 0x02
ARDUCHIP_TRIG = 0x41
CAP_DONE_MASK = 0x08

OV5642_CHIPID_HIGH = 0x300a
OV5642_CHIPID_LOW = 0x300b

# Image sizes for OV2640
OV2640_160x120 = 0
OV2640_176x144 = 1
OV2640_320x240 = 2
OV2640_352x288 = 3
OV2640_640x480 = 4
OV2640_800x600 = 5
OV2640_1024x768 = 6
OV2640_1280x1024 = 7
OV2640_1600x1200 = 8

# Image formats
BMP = 0
JPEG = 1
RAW = 2

# Light modes
Auto = 0
Sunny = 1
Cloudy = 2
Office = 3
Home = 4

# Special effects
Antique = 0
Bluish = 1
Greenish = 2
Reddish = 3
BW = 4
Negative = 5
BWnegative = 6
Normal = 7
Sepia = 8

# Brightness levels
Brightness4 = 0
Brightness3 = 1
Brightness2 = 2
Brightness1 = 3
Brightness0 = 4
Brightness_1 = 5
Brightness_2 = 6
Brightness_3 = 7
Brightness_4 = 8

# Saturation levels
Saturation4 = 0
Saturation3 = 1
Saturation2 = 2
Saturation1 = 3
Saturation0 = 4
Saturation_1 = 5
Saturation_2 = 6
Saturation_3 = 7
Saturation_4 = 8

# Contrast levels
Contrast4 = 0
Contrast3 = 1
Contrast2 = 2
Contrast1 = 3
Contrast0 = 4
Contrast_1 = 5
Contrast_2 = 6
Contrast_3 = 7
Contrast_4 = 8


class ArducamClass(object):
    def __init__(self, camera_type, cs_pin=17, i2c_bus=1, spi_bus=0, spi_device=0):
        """
        Initialize Arducam for Raspberry Pi 4
        
        Args:
            camera_type: OV2640 or OV5642
            cs_pin: GPIO pin for SPI CS (default: 17, BCM numbering)
            i2c_bus: I2C bus number (default: 1)
            spi_bus: SPI bus number (default: 0)
            spi_device: SPI device number (default: 0)
        """
        self.CameraMode = JPEG
        self.CameraType = camera_type
        self.cs_pin = cs_pin
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, GPIO.HIGH)
        
        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 4000000
        self.spi.mode = 0
        self.spi.no_cs = True  # We'll control CS manually with GPIO
        
        # Setup I2C
        self.i2c = smbus2.SMBus(i2c_bus)
        if camera_type == OV2640:
            self.I2cAddress = 0x30
        else:
            self.I2cAddress = 0x3c
        
        # Reset camera
        self.Spi_write(0x07, 0x80)
        time.sleep(0.1)
        self.Spi_write(0x07, 0x00)
        time.sleep(0.1)
    
    def __del__(self):
        """Cleanup GPIO and close connections"""
        try:
            self.spi.close()
            GPIO.cleanup(self.cs_pin)
        except:
            pass
    
    def Camera_Detection(self):
        """Detect and verify camera module"""
        while True:
            if self.CameraType == OV2640:
                self.I2cAddress = 0x30
                self.wrSensorReg8_8(0xff, 0x01)
                id_h = self.rdSensorReg8_8(0x0a)
                id_l = self.rdSensorReg8_8(0x0b)
                if (id_h == 0x26) and ((id_l == 0x40) or (id_l == 0x42)):
                    print('Camera detected: OV2640')
                    return True
                else:
                    print('Cannot find OV2640 module')
            elif self.CameraType == OV5642:
                self.I2cAddress = 0x3c
                self.wrSensorReg16_8(0xff, 0x01)
                id_h = self.rdSensorReg16_8(OV5642_CHIPID_HIGH)
                id_l = self.rdSensorReg16_8(OV5642_CHIPID_LOW)
                if (id_h == 0x56) and (id_l == 0x42):
                    print('Camera detected: OV5642')
                    return True
                else:
                    print('Cannot find OV5642 module')
            time.sleep(1)
    
    def Spi_Test(self):
        """Test SPI interface"""
        while True:
            self.Spi_write(0x00, 0x56)
            value = self.Spi_read(0x00)
            if value == 0x56:
                print('SPI interface OK')
                return True
            else:
                print('SPI interface Error')
            time.sleep(1)
    
    def Camera_Init(self):
        """Initialize camera with default settings"""
        if self.CameraType == OV2640:
            self.wrSensorReg8_8(0xff, 0x01)
            self.wrSensorReg8_8(0x12, 0x80)
            time.sleep(0.1)
            self.wrSensorRegs8_8(OV2640_JPEG_INIT)
            self.wrSensorRegs8_8(OV2640_YUV422)
            self.wrSensorRegs8_8(OV2640_JPEG)
            self.wrSensorReg8_8(0xff, 0x01)
            self.wrSensorReg8_8(0x15, 0x00)
            self.wrSensorRegs8_8(OV2640_320x240_JPEG)
    
    def Spi_write(self, address, value):
        """Write to SPI register"""
        GPIO.output(self.cs_pin, GPIO.LOW)
        self.spi.xfer2([address | 0x80, value])
        GPIO.output(self.cs_pin, GPIO.HIGH)
    
    def Spi_read(self, address):
        """Read from SPI register"""
        GPIO.output(self.cs_pin, GPIO.LOW)
        result = self.spi.xfer2([address & 0x7F, 0x00])
        GPIO.output(self.cs_pin, GPIO.HIGH)
        return result[1]
    
    def wrSensorReg8_8(self, addr, val):
        """Write 8-bit register address, 8-bit value"""
        try:
            self.i2c.write_byte_data(self.I2cAddress, addr, val)
        except Exception as e:
            print(f"I2C write error: {e}")
    
    def rdSensorReg8_8(self, addr):
        """Read 8-bit register address"""
        try:
            return self.i2c.read_byte_data(self.I2cAddress, addr)
        except Exception as e:
            print(f"I2C read error: {e}")
            return 0
    
    def wrSensorReg16_8(self, addr, val):
        """Write 16-bit register address, 8-bit value"""
        try:
            self.i2c.write_i2c_block_data(self.I2cAddress, (addr >> 8) & 0xff, [addr & 0xff, val])
            time.sleep(0.003)
        except Exception as e:
            print(f"I2C write error: {e}")
    
    def rdSensorReg16_8(self, addr):
        """Read 16-bit register address"""
        try:
            self.i2c.write_i2c_block_data(self.I2cAddress, (addr >> 8) & 0xff, [addr & 0xff])
            return self.i2c.read_byte(self.I2cAddress)
        except Exception as e:
            print(f"I2C read error: {e}")
            return 0
    
    def wrSensorRegs8_8(self, reg_list):
        """Write a list of 8-bit register/value pairs"""
        for reg in reg_list:
            addr = reg[0]
            val = reg[1]
            if (addr == 0xff and val == 0xff):
                return
            self.wrSensorReg8_8(addr, val)
            time.sleep(0.001)
    
    def wrSensorRegs16_8(self, reg_list):
        """Write a list of 16-bit register/value pairs"""
        for reg in reg_list:
            addr = reg[0]
            val = reg[1]
            if (addr == 0xffff and val == 0xff):
                return
            self.wrSensorReg16_8(addr, val)
    
    def get_bit(self, addr, bit):
        """Read register and return bitwise AND with bit mask"""
        value = self.Spi_read(addr)
        return value & bit
    
    def set_bit(self, addr, bit):
        """Clear bits at address"""
        temp = self.Spi_read(addr)
        self.Spi_write(addr, temp & (~bit))
    
    def clear_fifo_flag(self):
        """Clear FIFO write done flag"""
        self.Spi_write(0x04, 0x01)
    
    def flush_fifo(self):
        """Flush FIFO"""
        self.Spi_write(0x04, 0x01)
    
    def start_capture(self):
        """Start image capture"""
        self.Spi_write(0x04, 0x02)
    
    def read_fifo_length(self):
        """Read FIFO length"""
        len1 = self.Spi_read(0x42)
        len2 = self.Spi_read(0x43)
        len3 = self.Spi_read(0x44)
        len3 = len3 & 0x7f
        length = ((len3 << 16) | (len2 << 8) | len1) & 0x07fffff
        return length
    
    def read_fifo_burst(self, buffer_size=1024):
        """
        Read image data from FIFO in burst mode
        
        Args:
            buffer_size: Size of read buffer (default: 1024)
            
        Returns:
            bytearray containing image data
        """
        length = self.read_fifo_length()
        print(f"Image size: {length} bytes")
        
        if length == 0 or length > 0x7FFFFF:
            print(f"Warning: Invalid FIFO length: {length}")
            return bytearray()
        
        image_data = bytearray()
        
        # Start burst read - set CS low and send burst read command
        GPIO.output(self.cs_pin, GPIO.LOW)
        self.spi.xfer2([0x3C])  # Burst read command (with dummy byte to complete xfer)
        
        # Read image data in chunks
        bytes_read = 0
        dummy_buffer = [0x00] * buffer_size  # Reusable dummy buffer
        
        while bytes_read < length:
            bytes_to_read = min(buffer_size, length - bytes_read)
            
            # Read data bytes - send dummy bytes to clock out data
            if bytes_to_read == buffer_size:
                chunk = self.spi.xfer2(dummy_buffer)
            else:
                chunk = self.spi.xfer2([0x00] * bytes_to_read)
            
            image_data.extend(chunk)
            bytes_read += bytes_to_read
            
            # Print progress for large images
            if length > 10000 and (bytes_read % 10240 == 0 or bytes_read == length):
                print(f"  Progress: {bytes_read}/{length} bytes ({100*bytes_read//length}%)")
        
        # End burst read - set CS high
        GPIO.output(self.cs_pin, GPIO.HIGH)
        self.clear_fifo_flag()
        
        print(f"Read complete: {len(image_data)} bytes")
        
        return image_data
    
    def OV2640_set_JPEG_size(self, size):
        """Set JPEG image size for OV2640"""
        if size == OV2640_160x120:
            self.wrSensorRegs8_8(OV2640_160x120_JPEG)
        elif size == OV2640_176x144:
            self.wrSensorRegs8_8(OV2640_176x144_JPEG)
        elif size == OV2640_320x240:
            self.wrSensorRegs8_8(OV2640_320x240_JPEG)
        elif size == OV2640_352x288:
            self.wrSensorRegs8_8(OV2640_352x288_JPEG)
        elif size == OV2640_640x480:
            self.wrSensorRegs8_8(OV2640_640x480_JPEG)
        elif size == OV2640_800x600:
            self.wrSensorRegs8_8(OV2640_800x600_JPEG)
        elif size == OV2640_1024x768:
            self.wrSensorRegs8_8(OV2640_1024x768_JPEG)
        elif size == OV2640_1280x1024:
            self.wrSensorRegs8_8(OV2640_1280x1024_JPEG)
        elif size == OV2640_1600x1200:
            self.wrSensorRegs8_8(OV2640_1600x1200_JPEG)
        else:
            self.wrSensorRegs8_8(OV2640_320x240_JPEG)
    
    def OV2640_set_Light_Mode(self, mode):
        """Set light/white balance mode"""
        if mode == Auto:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0xc7, 0x00)
        elif mode == Sunny:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0xc7, 0x40)
            self.wrSensorReg8_8(0xcc, 0x5e)
            self.wrSensorReg8_8(0xcd, 0x41)
            self.wrSensorReg8_8(0xce, 0x54)
        elif mode == Cloudy:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0xc7, 0x40)
            self.wrSensorReg8_8(0xcc, 0x65)
            self.wrSensorReg8_8(0xcd, 0x41)
            self.wrSensorReg8_8(0xce, 0x4f)
        elif mode == Office:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0xc7, 0x40)
            self.wrSensorReg8_8(0xcc, 0x52)
            self.wrSensorReg8_8(0xcd, 0x41)
            self.wrSensorReg8_8(0xce, 0x66)
        elif mode == Home:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0xc7, 0x40)
            self.wrSensorReg8_8(0xcc, 0x42)
            self.wrSensorReg8_8(0xcd, 0x3f)
            self.wrSensorReg8_8(0xce, 0x71)
    
    def OV2640_set_Color_Saturation(self, saturation):
        """Set color saturation"""
        if saturation == Saturation2:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x02)
            self.wrSensorReg8_8(0x7c, 0x03)
            self.wrSensorReg8_8(0x7d, 0x68)
            self.wrSensorReg8_8(0x7d, 0x68)
        elif saturation == Saturation1:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x02)
            self.wrSensorReg8_8(0x7c, 0x03)
            self.wrSensorReg8_8(0x7d, 0x58)
            self.wrSensorReg8_8(0x7d, 0x58)
        elif saturation == Saturation0:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x02)
            self.wrSensorReg8_8(0x7c, 0x03)
            self.wrSensorReg8_8(0x7d, 0x48)
            self.wrSensorReg8_8(0x7d, 0x48)
    
    def OV2640_set_Brightness(self, brightness):
        """Set brightness level"""
        if brightness == Brightness2:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x09)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0x00)
        elif brightness == Brightness1:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x09)
            self.wrSensorReg8_8(0x7d, 0x30)
            self.wrSensorReg8_8(0x7d, 0x00)
        elif brightness == Brightness0:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x09)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x00)
    
    def OV2640_set_Contrast(self, contrast):
        """Set contrast level"""
        if contrast == Contrast2:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x07)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x28)
            self.wrSensorReg8_8(0x7d, 0x0c)
            self.wrSensorReg8_8(0x7d, 0x06)
        elif contrast == Contrast1:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x07)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x24)
            self.wrSensorReg8_8(0x7d, 0x16)
            self.wrSensorReg8_8(0x7d, 0x06)
        elif contrast == Contrast0:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x04)
            self.wrSensorReg8_8(0x7c, 0x07)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x20)
            self.wrSensorReg8_8(0x7d, 0x06)
    
    def OV2640_set_Special_effects(self, effect):
        """Set special effects"""
        if effect == Antique:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0xa6)
        elif effect == Bluish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0xa0)
            self.wrSensorReg8_8(0x7d, 0x40)
        elif effect == Greenish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0x40)
        elif effect == Reddish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0xc0)
        elif effect == BW:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif effect == Negative:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif effect == BWnegative:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x58)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif effect == Normal:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x00)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)

