#!/usr/bin/env python3
"""
Simple image capture script for Arducam OV2640 on Raspberry Pi 4
This script captures a single image and saves it as a JPEG file.
"""

import time
from datetime import datetime
from Arducam_RPI4 import ArducamClass, OV2640, OV2640_640x480

def capture_image(output_filename=None, resolution=OV2640_640x480):
    """
    Capture a single image from the Arducam OV2640
    
    Args:
        output_filename: Output file name (default: timestamp-based)
        resolution: Image resolution (default: 640x480)
    
    Returns:
        str: Path to saved image file
    """
    # Generate filename if not provided
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"capture_{timestamp}.jpg"
    
    print("Initializing camera...")
    
    # Initialize camera with OV2640
    # Default pins: CS=GPIO17, I2C bus=1, SPI bus=0
    camera = ArducamClass(OV2640)
    
    try:
        # Detect camera
        print("Detecting camera...")
        camera.Camera_Detection()
        
        # Test SPI interface
        print("Testing SPI interface...")
        camera.Spi_Test()
        
        # Initialize camera
        print("Initializing camera settings...")
        camera.Camera_Init()
        time.sleep(1)
        
        # Set resolution
        print(f"Setting resolution...")
        camera.OV2640_set_JPEG_size(resolution)
        time.sleep(0.5)
        
        # Clear FIFO
        camera.clear_fifo_flag()
        
        # Capture image
        print("Capturing image...")
        camera.flush_fifo()
        camera.clear_fifo_flag()
        camera.start_capture()
        
        # Wait for capture to complete (timeout after 5 seconds)
        timeout = 5
        start_time = time.time()
        while True:
            if camera.get_bit(0x41, 0x08) != 0:  # CAP_DONE_MASK
                break
            if time.time() - start_time > timeout:
                print("Error: Capture timeout!")
                return None
            time.sleep(0.01)
        
        print("Capture complete! Reading image data...")
        
        # Small delay before reading FIFO
        time.sleep(0.1)
        
        # Read image data from FIFO
        image_data = camera.read_fifo_burst()
        
        # Verify JPEG header
        if len(image_data) < 2:
            print("Error: Image data too small!")
            return None
        
        if image_data[0] == 0xFF and image_data[1] == 0xD8:
            print("✓ Valid JPEG header detected")
        else:
            print(f"⚠ Warning: Invalid JPEG header! Starts with 0x{image_data[0]:02X} 0x{image_data[1]:02X}")
            print("  Expected: 0xFF 0xD8 (JPEG start marker)")
            # Continue anyway, but user is warned
        
        # Save image to file
        with open(output_filename, 'wb') as f:
            f.write(image_data)
        
        print(f"Image saved: {output_filename}")
        print(f"File size: {len(image_data)} bytes")
        
        return output_filename
        
    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
        return None
    except Exception as e:
        print(f"Error during capture: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Cleanup
        del camera
        print("Camera cleanup complete")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Capture image from Arducam OV2640')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output filename (default: capture_TIMESTAMP.jpg)')
    parser.add_argument('-r', '--resolution', type=int, default=4,
                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                        help='Resolution: 0=160x120, 1=176x144, 2=320x240, 3=352x288, '
                             '4=640x480 (default), 5=800x600, 6=1024x768, 7=1280x1024, 8=1600x1200')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Arducam OV2640 Image Capture")
    print("=" * 50)
    
    result = capture_image(args.output, args.resolution)
    
    if result:
        print("\n✓ Success!")
    else:
        print("\n✗ Failed to capture image")

