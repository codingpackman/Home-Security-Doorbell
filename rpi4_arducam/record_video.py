#!/usr/bin/env python3
"""
Video recording script for Arducam OV2640 on Raspberry Pi 4
Records a series of JPEG frames and optionally compiles them into a video
"""

import time
import os
import subprocess
import shutil
from datetime import datetime
from Arducam_RPI4 import (
    ArducamClass, OV2640,
    OV2640_320x240, OV2640_640x480, OV2640_800x600
)

class VideoRecorder:
    def __init__(self, resolution=OV2640_640x480):
        """
        Initialize video recorder
        
        Args:
            resolution: Camera resolution (affects max frame rate)
        """
        print("Initializing camera for video recording...")
        self.camera = ArducamClass(OV2640)
        self.resolution = resolution
        
        # Detect and initialize
        print("Detecting camera...")
        self.camera.Camera_Detection()
        
        print("Testing SPI interface...")
        self.camera.Spi_Test()
        
        print("Initializing camera...")
        self.camera.Camera_Init()
        time.sleep(1)
        
        # Set resolution
        print(f"Setting resolution...")
        self.camera.OV2640_set_JPEG_size(resolution)
        time.sleep(0.5)
        
        print("Camera ready for recording!")
    
    def capture_frame(self, frame_number, output_dir):
        """
        Capture a single frame
        
        Args:
            frame_number: Frame number for filename
            output_dir: Directory to save frame
            
        Returns:
            tuple: (success, filename, capture_time)
        """
        start_time = time.time()
        
        try:
            # Clear FIFO
            self.camera.clear_fifo_flag()
            
            # Start capture
            self.camera.flush_fifo()
            self.camera.clear_fifo_flag()
            self.camera.start_capture()
            
            # Wait for capture to complete (timeout after 2 seconds)
            timeout_start = time.time()
            while True:
                if self.camera.get_bit(0x41, 0x08) != 0:
                    break
                if time.time() - timeout_start > 2:
                    return False, None, 0
                time.sleep(0.001)
            
            # Small delay before reading
            time.sleep(0.05)
            
            # Read image data
            image_data = self.camera.read_fifo_burst()
            
            # Verify JPEG header
            if len(image_data) < 2 or image_data[0] != 0xFF or image_data[1] != 0xD8:
                return False, None, 0
            
            # Save frame
            filename = os.path.join(output_dir, f"frame_{frame_number:05d}.jpg")
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            capture_time = time.time() - start_time
            return True, filename, capture_time
            
        except Exception as e:
            print(f"Error capturing frame {frame_number}: {e}")
            return False, None, 0
    
    def record_video(self, duration=10, target_fps=10, output_dir=None, 
                     output_video=None, cleanup_frames=True):
        """
        Record video by capturing frames
        
        Args:
            duration: Recording duration in seconds (default: 10)
            target_fps: Target frames per second (default: 10)
            output_dir: Directory for frames (default: temp folder)
            output_video: Output video filename (default: video_TIMESTAMP.mp4)
            cleanup_frames: Delete frames after creating video (default: True)
            
        Returns:
            str: Path to output video file or None on error
        """
        # Create output directory
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"video_frames_{timestamp}"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate output video filename
        if output_video is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video = f"video_{timestamp}.mp4"
        
        print(f"\n{'='*60}")
        print(f"Recording Video")
        print(f"{'='*60}")
        print(f"Duration: {duration} seconds")
        print(f"Target FPS: {target_fps}")
        print(f"Output: {output_video}")
        print(f"Frame storage: {output_dir}")
        print(f"{'='*60}\n")
        
        # Calculate timing
        frame_interval = 1.0 / target_fps
        total_frames = int(duration * target_fps)
        
        print(f"Starting recording... (press Ctrl+C to stop early)\n")
        
        captured_frames = []
        frame_times = []
        start_time = time.time()
        
        try:
            for frame_num in range(total_frames):
                frame_start = time.time()
                
                # Capture frame
                success, filename, capture_time = self.capture_frame(frame_num, output_dir)
                
                if success:
                    captured_frames.append(filename)
                    frame_times.append(capture_time)
                    
                    # Calculate stats
                    elapsed = time.time() - start_time
                    progress = (frame_num + 1) / total_frames * 100
                    actual_fps = (frame_num + 1) / elapsed if elapsed > 0 else 0
                    eta = (total_frames - frame_num - 1) / actual_fps if actual_fps > 0 else 0
                    
                    # Print progress
                    print(f"Frame {frame_num + 1:3d}/{total_frames} "
                          f"[{progress:5.1f}%] "
                          f"| FPS: {actual_fps:4.1f} "
                          f"| Capture: {capture_time*1000:5.1f}ms "
                          f"| ETA: {eta:4.1f}s", end='\r')
                else:
                    print(f"\nWarning: Failed to capture frame {frame_num}")
                
                # Wait for next frame (if needed)
                frame_elapsed = time.time() - frame_start
                sleep_time = frame_interval - frame_elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            print("\n\nRecording stopped by user")
        
        # Summary
        total_elapsed = time.time() - start_time
        actual_fps = len(captured_frames) / total_elapsed if total_elapsed > 0 else 0
        
        print(f"\n\n{'='*60}")
        print(f"Recording Complete")
        print(f"{'='*60}")
        print(f"Frames captured: {len(captured_frames)}/{total_frames}")
        print(f"Total time: {total_elapsed:.2f} seconds")
        print(f"Average FPS: {actual_fps:.2f}")
        if frame_times:
            print(f"Avg capture time: {sum(frame_times)/len(frame_times)*1000:.1f}ms")
            print(f"Min capture time: {min(frame_times)*1000:.1f}ms")
            print(f"Max capture time: {max(frame_times)*1000:.1f}ms")
        print(f"{'='*60}\n")
        
        if len(captured_frames) == 0:
            print("No frames captured! Cannot create video.")
            return None
        
        # Create video from frames
        print("Creating video from frames...")
        video_path = self.create_video_ffmpeg(output_dir, output_video, actual_fps)
        
        if video_path and cleanup_frames:
            print(f"Cleaning up frame files...")
            try:
                shutil.rmtree(output_dir)
                print(f"✓ Removed {output_dir}")
            except Exception as e:
                print(f"Warning: Could not remove frame directory: {e}")
        
        return video_path
    
    def create_video_ffmpeg(self, frames_dir, output_file, fps):
        """
        Create video from frames using ffmpeg
        
        Args:
            frames_dir: Directory containing frame_*.jpg files
            output_file: Output video filename
            fps: Frames per second
            
        Returns:
            str: Path to video file or None on error
        """
        # Check if ffmpeg is available
        if not shutil.which('ffmpeg'):
            print("✗ ffmpeg not found!")
            print("  Install with: sudo apt-get install ffmpeg")
            print(f"  Frames saved in: {frames_dir}")
            return None
        
        try:
            # Build ffmpeg command
            # Input: frame_%05d.jpg (frame_00000.jpg, frame_00001.jpg, ...)
            # Output: H.264 encoded MP4 video
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file
                '-framerate', str(fps),
                '-i', os.path.join(frames_dir, 'frame_%05d.jpg'),
                '-c:v', 'libx264',  # H.264 codec
                '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                '-preset', 'medium',  # Encoding speed
                '-crf', '23',  # Quality (lower = better, 23 is default)
                output_file
            ]
            
            print(f"Running ffmpeg...")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"✓ Video created: {output_file}")
                    print(f"  Size: {file_size / 1024 / 1024:.2f} MB")
                    return output_file
                else:
                    print("✗ Video file not created")
                    return None
            else:
                print(f"✗ ffmpeg error:")
                print(result.stderr)
                return None
                
        except Exception as e:
            print(f"✗ Error creating video: {e}")
            return None
    
    def cleanup(self):
        """Cleanup camera resources"""
        del self.camera


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Record video with Arducam OV2640',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record 10 second video at 10 FPS (default)
  python3 record_video.py
  
  # Record 30 second video at 15 FPS
  python3 record_video.py -d 30 --fps 15
  
  # Record at lower resolution for higher frame rate
  python3 record_video.py -r 320x240 --fps 20
  
  # Record and keep frame files
  python3 record_video.py --keep-frames
  
  # Custom output filename
  python3 record_video.py -o myvideo.mp4

Notes:
  - Lower resolutions allow higher frame rates
  - Typical FPS: 320x240 → 15-20 FPS, 640x480 → 8-12 FPS
  - Requires ffmpeg: sudo apt-get install ffmpeg
        """)
    
    parser.add_argument('-d', '--duration', type=float, default=10,
                        help='Recording duration in seconds (default: 10)')
    parser.add_argument('--fps', type=float, default=10,
                        help='Target frames per second (default: 10)')
    parser.add_argument('-r', '--resolution', type=str, default='640x480',
                        choices=['320x240', '640x480', '800x600'],
                        help='Video resolution (default: 640x480)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output video filename (default: video_TIMESTAMP.mp4)')
    parser.add_argument('--keep-frames', action='store_true',
                        help='Keep individual frame files after creating video')
    parser.add_argument('--frames-dir', type=str, default=None,
                        help='Directory for frame storage (default: temp folder)')
    
    args = parser.parse_args()
    
    # Map resolution string to constant
    resolution_map = {
        '320x240': OV2640_320x240,
        '640x480': OV2640_640x480,
        '800x600': OV2640_800x600
    }
    
    print("=" * 60)
    print("Arducam OV2640 Video Recorder")
    print("=" * 60)
    
    try:
        # Initialize recorder
        recorder = VideoRecorder(resolution=resolution_map[args.resolution])
        
        # Record video
        video_file = recorder.record_video(
            duration=args.duration,
            target_fps=args.fps,
            output_dir=args.frames_dir,
            output_video=args.output,
            cleanup_frames=not args.keep_frames
        )
        
        # Summary
        if video_file:
            print(f"\n{'='*60}")
            print("✓ Success!")
            print(f"{'='*60}")
            print(f"Video: {video_file}")
            print(f"\nPlay with:")
            print(f"  vlc {video_file}")
            print(f"  mpv {video_file}")
            print(f"  omxplayer {video_file}  # On Raspberry Pi")
            print(f"{'='*60}")
        else:
            print(f"\n{'='*60}")
            print("✗ Failed to create video")
            print(f"{'='*60}")
        
        # Cleanup
        recorder.cleanup()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

