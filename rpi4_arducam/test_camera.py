#!/usr/bin/env python3
"""
Camera diagnostic and test script for Arducam OV2640
Use this to verify your camera is working correctly
"""

import time
import sys
from Arducam_RPI4 import ArducamClass, OV2640

def test_spi_register():
    """Test SPI communication by reading/writing a test register"""
    print("\n" + "="*60)
    print("TEST 1: SPI Register Read/Write")
    print("="*60)
    
    camera = ArducamClass(OV2640)
    
    # Test writing and reading back
    test_value = 0x56
    camera.Spi_write(0x00, test_value)
    read_value = camera.Spi_read(0x00)
    
    print(f"Wrote: 0x{test_value:02X}")
    print(f"Read:  0x{read_value:02X}")
    
    if read_value == test_value:
        print("✓ SPI communication OK!")
        return True
    else:
        print("✗ SPI communication FAILED!")
        print("  Check your wiring:")
        print("  - CS, MOSI, MISO, SCK connections")
        print("  - Power (3.3V) and Ground")
        return False

def test_i2c_detection():
    """Test I2C camera detection"""
    print("\n" + "="*60)
    print("TEST 2: I2C Camera Detection")
    print("="*60)
    
    camera = ArducamClass(OV2640)
    
    # Read camera ID registers
    camera.wrSensorReg8_8(0xff, 0x01)
    id_h = camera.rdSensorReg8_8(0x0a)
    id_l = camera.rdSensorReg8_8(0x0b)
    
    print(f"Camera ID High: 0x{id_h:02X} (expected: 0x26)")
    print(f"Camera ID Low:  0x{id_l:02X} (expected: 0x40 or 0x42)")
    
    if id_h == 0x26 and (id_l == 0x40 or id_l == 0x42):
        print("✓ OV2640 camera detected!")
        return True
    else:
        print("✗ Camera NOT detected!")
        print("  Check your wiring:")
        print("  - SDA and SCL connections")
        print("  - I2C is enabled (run: sudo raspi-config)")
        print("  - Try: sudo i2cdetect -y 1")
        return False

def test_fifo_operations():
    """Test FIFO operations"""
    print("\n" + "="*60)
    print("TEST 3: FIFO Operations")
    print("="*60)
    
    camera = ArducamClass(OV2640)
    camera.Camera_Detection()
    camera.Camera_Init()
    time.sleep(1)
    
    # Clear FIFO
    camera.clear_fifo_flag()
    print("✓ FIFO cleared")
    
    # Start capture
    camera.flush_fifo()
    camera.clear_fifo_flag()
    camera.start_capture()
    print("✓ Capture started")
    
    # Wait for capture
    timeout = 5
    start_time = time.time()
    captured = False
    
    while time.time() - start_time < timeout:
        if camera.get_bit(0x41, 0x08) != 0:
            captured = True
            break
        time.sleep(0.01)
    
    if captured:
        length = camera.read_fifo_length()
        print(f"✓ Capture complete! FIFO size: {length} bytes")
        
        if length > 0 and length < 0x7FFFFF:
            print(f"✓ FIFO length is valid")
            return True
        else:
            print(f"✗ FIFO length invalid: {length}")
            return False
    else:
        print("✗ Capture timeout!")
        print("  Camera may not be properly initialized")
        return False

def test_jpeg_header():
    """Test capturing and checking JPEG header"""
    print("\n" + "="*60)
    print("TEST 4: JPEG Image Capture")
    print("="*60)
    
    camera = ArducamClass(OV2640)
    camera.Camera_Detection()
    camera.Camera_Init()
    time.sleep(1)
    
    # Set resolution
    from Arducam_RPI4 import OV2640_320x240
    camera.OV2640_set_JPEG_size(OV2640_320x240)
    time.sleep(0.5)
    
    # Capture
    camera.clear_fifo_flag()
    camera.flush_fifo()
    camera.clear_fifo_flag()
    camera.start_capture()
    
    # Wait for capture
    timeout = 5
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if camera.get_bit(0x41, 0x08) != 0:
            break
        time.sleep(0.01)
    else:
        print("✗ Capture timeout!")
        return False
    
    time.sleep(0.1)
    
    # Read data
    print("Reading FIFO data...")
    image_data = camera.read_fifo_burst()
    
    if len(image_data) < 2:
        print(f"✗ Image too small: {len(image_data)} bytes")
        return False
    
    # Check JPEG header
    print(f"\nFirst 16 bytes of captured data:")
    hex_str = " ".join([f"{b:02X}" for b in image_data[:16]])
    print(f"  {hex_str}")
    
    if image_data[0] == 0xFF and image_data[1] == 0xD8:
        print("✓ Valid JPEG header (0xFF 0xD8)")
        
        # Check for JPEG end marker
        if len(image_data) > 2 and image_data[-2] == 0xFF and image_data[-1] == 0xD9:
            print("✓ Valid JPEG end marker (0xFF 0xD9)")
            
            # Save test image
            with open('test_image.jpg', 'wb') as f:
                f.write(image_data)
            print(f"✓ Test image saved: test_image.jpg ({len(image_data)} bytes)")
            print("\nTry opening test_image.jpg to verify!")
            return True
        else:
            print("⚠ JPEG end marker not found (may still be valid)")
            # Save anyway
            with open('test_image.jpg', 'wb') as f:
                f.write(image_data)
            print(f"⚠ Test image saved: test_image.jpg ({len(image_data)} bytes)")
            return True
    else:
        print(f"✗ Invalid JPEG header!")
        print(f"  Expected: FF D8")
        print(f"  Got:      {image_data[0]:02X} {image_data[1]:02X}")
        
        # Save for analysis
        with open('test_image_raw.bin', 'wb') as f:
            f.write(image_data)
        print(f"  Raw data saved to test_image_raw.bin for analysis")
        return False

def main():
    print("="*60)
    print("Arducam OV2640 Diagnostic Tool")
    print("="*60)
    print("\nThis script will test your camera setup step by step.")
    print("Please ensure:")
    print("  - Camera is properly wired")
    print("  - SPI and I2C are enabled")
    print("  - Using 3.3V power (NOT 5V!)")
    
    input("\nPress Enter to start tests...")
    
    results = []
    
    # Run tests
    try:
        results.append(("SPI Communication", test_spi_register()))
        results.append(("I2C Camera Detection", test_i2c_detection()))
        results.append(("FIFO Operations", test_fifo_operations()))
        results.append(("JPEG Capture", test_jpeg_header()))
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error during tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("="*60)
    if all_passed:
        print("✓ All tests passed! Your camera is working correctly.")
        print("\nYou can now use:")
        print("  python3 capture_image.py")
        print("  python3 capture_advanced.py")
    else:
        print("✗ Some tests failed. Please check:")
        print("  1. Wiring connections (see WIRING.md)")
        print("  2. SPI enabled: ls /dev/spi*")
        print("  3. I2C enabled: ls /dev/i2c*")
        print("  4. Camera detected: sudo i2cdetect -y 1")
        print("  5. Power is 3.3V (NOT 5V!)")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

