#!/usr/bin/env python3
"""
Advanced image capture script for Arducam OV2640 on Raspberry Pi 4
Includes options for image effects, lighting modes, and continuous capture
"""

import time
from datetime import datetime
from Arducam_RPI4 import (
    ArducamClass, OV2640, 
    OV2640_160x120, OV2640_176x144, OV2640_320x240, OV2640_352x288,
    OV2640_640x480, OV2640_800x600, OV2640_1024x768, OV2640_1280x1024, OV2640_1600x1200,
    Auto, Sunny, Cloudy, Office, Home,
    Normal, Antique, Bluish, Greenish, Reddish, BW, Negative, Sepia,
    Brightness0, Brightness1, Brightness2, Brightness_1, Brightness_2,
    Contrast0, Contrast1, Contrast2, Contrast_1, Contrast_2,
    Saturation0, Saturation1, Saturation2, Saturation_1, Saturation_2
)

# Resolution mapping
RESOLUTIONS = {
    '160x120': OV2640_160x120,
    '176x144': OV2640_176x144,
    '320x240': OV2640_320x240,
    '352x288': OV2640_352x288,
    '640x480': OV2640_640x480,
    '800x600': OV2640_800x600,
    '1024x768': OV2640_1024x768,
    '1280x1024': OV2640_1280x1024,
    '1600x1200': OV2640_1600x1200
}

# Light mode mapping
LIGHT_MODES = {
    'auto': Auto,
    'sunny': Sunny,
    'cloudy': Cloudy,
    'office': Office,
    'home': Home
}

# Special effects mapping
EFFECTS = {
    'normal': Normal,
    'antique': Antique,
    'bluish': Bluish,
    'greenish': Greenish,
    'reddish': Reddish,
    'bw': BW,
    'negative': Negative,
    'sepia': Sepia
}


class AdvancedCamera:
    def __init__(self):
        """Initialize camera"""
        print("Initializing Arducam OV2640...")
        self.camera = ArducamClass(OV2640)
        
        # Detect and initialize
        print("Detecting camera...")
        self.camera.Camera_Detection()
        
        print("Testing SPI interface...")
        self.camera.Spi_Test()
        
        print("Initializing camera...")
        self.camera.Camera_Init()
        time.sleep(1)
        
        print("Camera ready!")
    
    def configure(self, resolution='640x480', light_mode='auto', effect='normal',
                  brightness=None, contrast=None, saturation=None):
        """
        Configure camera settings
        
        Args:
            resolution: Image resolution (e.g., '640x480')
            light_mode: Light/white balance mode
            effect: Special effect to apply
            brightness: Brightness level (-2 to 2, None for default)
            contrast: Contrast level (-2 to 2, None for default)
            saturation: Saturation level (-2 to 2, None for default)
        """
        print(f"\nConfiguring camera:")
        print(f"  Resolution: {resolution}")
        print(f"  Light mode: {light_mode}")
        print(f"  Effect: {effect}")
        
        # Set resolution
        if resolution in RESOLUTIONS:
            self.camera.OV2640_set_JPEG_size(RESOLUTIONS[resolution])
        else:
            print(f"Warning: Unknown resolution '{resolution}', using 640x480")
            self.camera.OV2640_set_JPEG_size(OV2640_640x480)
        
        # Set light mode
        if light_mode in LIGHT_MODES:
            self.camera.OV2640_set_Light_Mode(LIGHT_MODES[light_mode])
        
        # Set special effect
        if effect in EFFECTS:
            self.camera.OV2640_set_Special_effects(EFFECTS[effect])
        
        # Set brightness
        if brightness is not None:
            brightness_map = {
                -2: Brightness_2, -1: Brightness_1, 0: Brightness0,
                1: Brightness1, 2: Brightness2
            }
            if brightness in brightness_map:
                print(f"  Brightness: {brightness}")
                self.camera.OV2640_set_Brightness(brightness_map[brightness])
        
        # Set contrast
        if contrast is not None:
            contrast_map = {
                -2: Contrast_2, -1: Contrast_1, 0: Contrast0,
                1: Contrast1, 2: Contrast2
            }
            if contrast in contrast_map:
                print(f"  Contrast: {contrast}")
                self.camera.OV2640_set_Contrast(contrast_map[contrast])
        
        # Set saturation
        if saturation is not None:
            saturation_map = {
                -2: Saturation_2, -1: Saturation_1, 0: Saturation0,
                1: Saturation1, 2: Saturation2
            }
            if saturation in saturation_map:
                print(f"  Saturation: {saturation}")
                self.camera.OV2640_set_Color_Saturation(saturation_map[saturation])
        
        time.sleep(0.5)
    
    def capture(self, output_filename=None):
        """
        Capture a single image
        
        Args:
            output_filename: Output file name
            
        Returns:
            str: Path to saved image or None on error
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"capture_{timestamp}.jpg"
        
        try:
            # Clear FIFO
            self.camera.clear_fifo_flag()
            
            # Start capture
            self.camera.flush_fifo()
            self.camera.clear_fifo_flag()
            self.camera.start_capture()
            
            # Wait for capture to complete
            timeout = 5
            start_time = time.time()
            while True:
                if self.camera.get_bit(0x41, 0x08) != 0:
                    break
                if time.time() - start_time > timeout:
                    print("Error: Capture timeout!")
                    return None
                time.sleep(0.01)
            
            # Small delay before reading FIFO
            time.sleep(0.1)
            
            # Read image data
            image_data = self.camera.read_fifo_burst()
            
            # Verify JPEG header
            if len(image_data) >= 2:
                if image_data[0] != 0xFF or image_data[1] != 0xD8:
                    print(f"  ⚠ Warning: Invalid JPEG header (0x{image_data[0]:02X} 0x{image_data[1]:02X})")
            
            # Save image
            with open(output_filename, 'wb') as f:
                f.write(image_data)
            
            return output_filename
            
        except Exception as e:
            print(f"Error capturing image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def continuous_capture(self, interval=1, count=10, prefix="capture"):
        """
        Capture multiple images at regular intervals
        
        Args:
            interval: Time between captures in seconds
            count: Number of images to capture
            prefix: Filename prefix
        """
        print(f"\nStarting continuous capture:")
        print(f"  Interval: {interval}s")
        print(f"  Count: {count} images")
        
        captured = []
        
        try:
            for i in range(count):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{prefix}_{i+1:03d}_{timestamp}.jpg"
                
                print(f"\n[{i+1}/{count}] Capturing {filename}...")
                result = self.capture(filename)
                
                if result:
                    print(f"  ✓ Saved ({len(open(result, 'rb').read())} bytes)")
                    captured.append(result)
                else:
                    print(f"  ✗ Failed")
                
                if i < count - 1:
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\nCapture interrupted by user")
        
        print(f"\n\nCapture complete: {len(captured)}/{count} images saved")
        return captured
    
    def cleanup(self):
        """Cleanup camera resources"""
        del self.camera


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Advanced image capture for Arducam OV2640',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture single image at 1600x1200
  python3 capture_advanced.py -r 1600x1200 -o photo.jpg
  
  # Capture with sepia effect and office lighting
  python3 capture_advanced.py -e sepia -l office
  
  # Capture 5 images at 2 second intervals
  python3 capture_advanced.py --continuous 5 --interval 2
  
  # Capture with custom brightness and contrast
  python3 capture_advanced.py --brightness 1 --contrast -1
        """)
    
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output filename for single capture')
    parser.add_argument('-r', '--resolution', type=str, default='640x480',
                        choices=list(RESOLUTIONS.keys()),
                        help='Image resolution (default: 640x480)')
    parser.add_argument('-l', '--light', type=str, default='auto',
                        choices=list(LIGHT_MODES.keys()),
                        help='Light/white balance mode (default: auto)')
    parser.add_argument('-e', '--effect', type=str, default='normal',
                        choices=list(EFFECTS.keys()),
                        help='Special effect (default: normal)')
    parser.add_argument('--brightness', type=int, choices=[-2, -1, 0, 1, 2],
                        help='Brightness level (-2 to 2)')
    parser.add_argument('--contrast', type=int, choices=[-2, -1, 0, 1, 2],
                        help='Contrast level (-2 to 2)')
    parser.add_argument('--saturation', type=int, choices=[-2, -1, 0, 1, 2],
                        help='Saturation level (-2 to 2)')
    parser.add_argument('--continuous', type=int, metavar='COUNT',
                        help='Capture COUNT images continuously')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Interval between continuous captures in seconds (default: 1.0)')
    parser.add_argument('--prefix', type=str, default='capture',
                        help='Filename prefix for continuous capture (default: capture)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Arducam OV2640 Advanced Image Capture")
    print("=" * 60)
    
    try:
        # Initialize camera
        cam = AdvancedCamera()
        
        # Configure settings
        cam.configure(
            resolution=args.resolution,
            light_mode=args.light,
            effect=args.effect,
            brightness=args.brightness,
            contrast=args.contrast,
            saturation=args.saturation
        )
        
        # Capture image(s)
        if args.continuous:
            # Continuous capture mode
            cam.continuous_capture(
                interval=args.interval,
                count=args.continuous,
                prefix=args.prefix
            )
        else:
            # Single capture mode
            print("\nCapturing image...")
            result = cam.capture(args.output)
            
            if result:
                file_size = len(open(result, 'rb').read())
                print(f"\n✓ Success!")
                print(f"  File: {result}")
                print(f"  Size: {file_size} bytes")
            else:
                print("\n✗ Failed to capture image")
        
        # Cleanup
        cam.cleanup()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

