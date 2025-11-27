#!/usr/bin/env python3
"""
Time-lapse recording script for Arducam OV2640
Captures frames at specified intervals - no ffmpeg required
Perfect for time-lapse photography
"""

import time
import os
from datetime import datetime
from Arducam_RPI4 import (
    ArducamClass, OV2640,
    OV2640_320x240, OV2640_640x480, OV2640_800x600, OV2640_1024x768, OV2640_1600x1200
)

def record_timelapse(duration=60, interval=1, resolution=OV2640_640x480, output_dir=None):
    """
    Record time-lapse by capturing frames at intervals
    
    Args:
        duration: Total recording duration in seconds
        interval: Interval between frames in seconds
        resolution: Image resolution
        output_dir: Output directory for frames
        
    Returns:
        int: Number of frames captured
    """
    # Create output directory
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"timelapse_{timestamp}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n{'='*60}")
    print("Time-Lapse Recording")
    print(f"{'='*60}")
    print(f"Duration: {duration} seconds")
    print(f"Interval: {interval} seconds")
    print(f"Output: {output_dir}/")
    print(f"Estimated frames: {int(duration / interval)}")
    print(f"{'='*60}\n")
    
    # Initialize camera
    print("Initializing camera...")
    camera = ArducamClass(OV2640)
    camera.Camera_Detection()
    camera.Spi_Test()
    camera.Camera_Init()
    time.sleep(1)
    
    camera.OV2640_set_JPEG_size(resolution)
    time.sleep(0.5)
    
    print("Camera ready!\n")
    print("Starting recording... (press Ctrl+C to stop early)\n")
    
    frame_count = 0
    start_time = time.time()
    next_capture = start_time
    
    try:
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Check if we've reached duration
            if elapsed >= duration:
                break
            
            # Check if it's time for next capture
            if current_time >= next_capture:
                # Capture frame
                camera.clear_fifo_flag()
                camera.flush_fifo()
                camera.clear_fifo_flag()
                camera.start_capture()
                
                # Wait for capture
                timeout = 3
                capture_start = time.time()
                while True:
                    if camera.get_bit(0x41, 0x08) != 0:
                        break
                    if time.time() - capture_start > timeout:
                        print(f"\nFrame {frame_count}: Capture timeout!")
                        break
                    time.sleep(0.001)
                else:
                    time.sleep(0.05)
                    
                    # Read and save frame
                    image_data = camera.read_fifo_burst()
                    
                    if len(image_data) >= 2 and image_data[0] == 0xFF and image_data[1] == 0xD8:
                        filename = os.path.join(output_dir, f"frame_{frame_count:05d}.jpg")
                        with open(filename, 'wb') as f:
                            f.write(image_data)
                        
                        # Print progress
                        remaining = duration - elapsed
                        progress = (elapsed / duration) * 100
                        print(f"Frame {frame_count:3d} | "
                              f"Time: {elapsed:6.1f}s / {duration:.0f}s | "
                              f"Progress: {progress:5.1f}% | "
                              f"Remaining: {remaining:5.1f}s", end='\r')
                        
                        frame_count += 1
                
                # Schedule next capture
                next_capture += interval
            
            # Small sleep to avoid busy waiting
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n\nRecording stopped by user")
    
    elapsed = time.time() - start_time
    
    print(f"\n\n{'='*60}")
    print("Recording Complete")
    print(f"{'='*60}")
    print(f"Frames captured: {frame_count}")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Average interval: {elapsed/frame_count:.2f}s" if frame_count > 0 else "N/A")
    print(f"Frames saved in: {output_dir}/")
    print(f"{'='*60}\n")
    
    # Cleanup
    del camera
    
    # Show conversion commands
    if frame_count > 0:
        print("To create a video from these frames:")
        print(f"\n  # Create MP4 video (30 FPS)")
        print(f"  ffmpeg -framerate 30 -i {output_dir}/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p output.mp4")
        print(f"\n  # Create GIF animation (10 FPS)")
        print(f"  ffmpeg -framerate 10 -i {output_dir}/frame_%05d.jpg output.gif")
        print(f"\n  # Create MP4 video with custom speed")
        print(f"  ffmpeg -framerate 60 -i {output_dir}/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p fast.mp4")
        print()
    
    return frame_count


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Record time-lapse with Arducam OV2640',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record 60 seconds, one frame per second
  python3 record_timelapse.py -d 60 -i 1
  
  # Time-lapse: 10 minutes, frame every 5 seconds
  python3 record_timelapse.py -d 600 -i 5
  
  # High-res time-lapse: 1 hour, frame every 30 seconds
  python3 record_timelapse.py -d 3600 -i 30 -r 1600x1200
  
  # Fast capture: 30 seconds, frame every 0.5 seconds
  python3 record_timelapse.py -d 30 -i 0.5 -r 320x240

After recording, create video with ffmpeg:
  ffmpeg -framerate 30 -i timelapse_*/frame_%05d.jpg -c:v libx264 -pix_fmt yuv420p video.mp4
        """)
    
    parser.add_argument('-d', '--duration', type=float, default=60,
                        help='Recording duration in seconds (default: 60)')
    parser.add_argument('-i', '--interval', type=float, default=1,
                        help='Interval between frames in seconds (default: 1)')
    parser.add_argument('-r', '--resolution', type=str, default='640x480',
                        choices=['320x240', '640x480', '800x600', '1024x768', '1600x1200'],
                        help='Image resolution (default: 640x480)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output directory (default: timelapse_TIMESTAMP)')
    
    args = parser.parse_args()
    
    # Map resolution string to constant
    resolution_map = {
        '320x240': OV2640_320x240,
        '640x480': OV2640_640x480,
        '800x600': OV2640_800x600,
        '1024x768': OV2640_1024x768,
        '1600x1200': OV2640_1600x1200
    }
    
    print("=" * 60)
    print("Arducam OV2640 Time-Lapse Recorder")
    print("=" * 60)
    
    try:
        frame_count = record_timelapse(
            duration=args.duration,
            interval=args.interval,
            resolution=resolution_map[args.resolution],
            output_dir=args.output
        )
        
        if frame_count > 0:
            print("✓ Success!")
        else:
            print("✗ No frames captured")
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

