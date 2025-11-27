#!/usr/bin/env python3
"""
Camera Controller Module for Smart Doorbell
Handles video recording using Arducam OV2640
This module is designed to be imported by main_system.py
"""

import os
import sys
import time
from datetime import datetime

# Add rpi4_arducam directory to path so we can import the camera module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARDUCAM_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'rpi4_arducam')
sys.path.insert(0, ARDUCAM_DIR)

try:
    from Arducam_RPI4 import ArducamClass, OV2640, OV2640_640x480
    CAMERA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Arducam module: {e}")
    print("Camera recording will not be available.")
    CAMERA_AVAILABLE = False


class CameraController:
    """Controls the Arducam for video recording"""
    
    def __init__(self, output_directory="./recordings", resolution=None):
        """
        Initialize the camera controller
        
        Args:
            output_directory: Directory to save recorded videos
            resolution: Camera resolution (default: OV2640_640x480)
        """
        self.output_directory = output_directory
        self.resolution = resolution if resolution else OV2640_640x480
        self.camera = None
        self.is_initialized = False
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            print(f"Created recordings directory: {output_directory}")
    
    def initialize_camera(self):
        """Initialize the camera hardware"""
        if not CAMERA_AVAILABLE:
            print("Camera module not available. Cannot initialize.")
            return False
        
        if self.is_initialized:
            print("Camera already initialized.")
            return True
        
        try:
            print("Initializing Arducam...")
            self.camera = ArducamClass(OV2640)
            
            print("Detecting camera...")
            self.camera.Camera_Detection()
            
            print("Testing SPI interface...")
            self.camera.Spi_Test()
            
            print("Initializing camera...")
            self.camera.Camera_Init()
            time.sleep(1)
            
            print("Setting resolution...")
            self.camera.OV2640_set_JPEG_size(self.resolution)
            time.sleep(0.5)
            
            self.is_initialized = True
            print("Camera initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.is_initialized = False
            return False
    
    def capture_frame(self, frame_number, frames_dir):
        """
        Capture a single frame
        
        Args:
            frame_number: Frame number for filename
            frames_dir: Directory to save the frame
            
        Returns:
            tuple: (success, filename, capture_time)
        """
        if not self.is_initialized:
            return False, None, 0
        
        start_time = time.time()
        
        try:
            # Clear FIFO
            self.camera.clear_fifo_flag()
            
            # Start capture
            self.camera.flush_fifo()
            self.camera.clear_fifo_flag()
            self.camera.start_capture()
            
            # Wait for capture to complete
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
            filename = os.path.join(frames_dir, f"frame_{frame_number:05d}.jpg")
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            capture_time = time.time() - start_time
            return True, filename, capture_time
            
        except Exception as e:
            print(f"Error capturing frame {frame_number}: {e}")
            return False, None, 0
    
    def record_video(self, event_type, duration=15, target_fps=10):
        """
        Record a video for the specified duration
        
        Args:
            event_type: Type of event ("motion" or "button_press")
            duration: Recording duration in seconds (default: 15)
            target_fps: Target frames per second (default: 10)
            
        Returns:
            str: Path to recorded video file or None on error
        """
        if not self.is_initialized:
            print("Camera not initialized. Attempting to initialize...")
            if not self.initialize_camera():
                print("Failed to initialize camera. Cannot record.")
                return None
        
        # Generate filename with timestamp and event type
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if event_type.lower() == "motion":
            video_name = f"motion_detected_{timestamp}.mp4"
        elif event_type.lower() == "button_press" or event_type.lower() == "doorbell":
            video_name = f"button_pressed_{timestamp}.mp4"
        else:
            video_name = f"recording_{timestamp}.mp4"
        
        output_video = os.path.join(self.output_directory, video_name)
        frames_dir = os.path.join(self.output_directory, f"frames_{timestamp}")
        
        # Create frames directory
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        
        print(f"\n{'='*60}")
        print(f"Recording Video: {event_type}")
        print(f"{'='*60}")
        print(f"Duration: {duration} seconds")
        print(f"Target FPS: {target_fps}")
        print(f"Output: {video_name}")
        print(f"{'='*60}\n")
        
        # Calculate timing
        frame_interval = 1.0 / target_fps
        total_frames = int(duration * target_fps)
        
        captured_frames = []
        start_time = time.time()
        
        try:
            for frame_num in range(total_frames):
                frame_start = time.time()
                
                # Capture frame
                success, filename, capture_time = self.capture_frame(frame_num, frames_dir)
                
                if success:
                    captured_frames.append(filename)
                    
                    # Calculate progress
                    elapsed = time.time() - start_time
                    progress = (frame_num + 1) / total_frames * 100
                    actual_fps = (frame_num + 1) / elapsed if elapsed > 0 else 0
                    
                    # Print progress (every 10 frames to reduce console spam)
                    if (frame_num + 1) % 10 == 0:
                        print(f"Progress: {progress:.1f}% | Frames: {frame_num + 1}/{total_frames} | FPS: {actual_fps:.1f}")
                
                # Wait for next frame
                frame_elapsed = time.time() - frame_start
                sleep_time = frame_interval - frame_elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        except Exception as e:
            print(f"\nError during recording: {e}")
        
        # Summary
        total_elapsed = time.time() - start_time
        actual_fps = len(captured_frames) / total_elapsed if total_elapsed > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"Recording Complete")
        print(f"{'='*60}")
        print(f"Frames captured: {len(captured_frames)}/{total_frames}")
        print(f"Total time: {total_elapsed:.2f} seconds")
        print(f"Average FPS: {actual_fps:.2f}")
        print(f"{'='*60}\n")
        
        if len(captured_frames) == 0:
            print("No frames captured! Cannot create video.")
            return None
        
        # Create video from frames
        print("Creating video from frames...")
        video_path = self._create_video_ffmpeg(frames_dir, output_video, actual_fps)
        
        # Cleanup frame files
        if video_path:
            print(f"Cleaning up frame files...")
            try:
                import shutil
                shutil.rmtree(frames_dir)
                print(f"✓ Removed {frames_dir}")
            except Exception as e:
                print(f"Warning: Could not remove frame directory: {e}")
        
        return video_path
    
    def _create_video_ffmpeg(self, frames_dir, output_file, fps):
        """
        Create video from frames using ffmpeg
        
        Args:
            frames_dir: Directory containing frame_*.jpg files
            output_file: Output video filename
            fps: Frames per second
            
        Returns:
            str: Path to video file or None on error
        """
        import subprocess
        import shutil
        
        # Check if ffmpeg is available
        if not shutil.which('ffmpeg'):
            print("✗ ffmpeg not found!")
            print("  Install with: sudo apt-get install ffmpeg")
            print(f"  Frames saved in: {frames_dir}")
            return None
        
        try:
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file
                '-framerate', str(fps),
                '-i', os.path.join(frames_dir, 'frame_%05d.jpg'),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-preset', 'medium',
                '-crf', '23',
                output_file
            ]
            
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
        if self.camera:
            del self.camera
            self.camera = None
        self.is_initialized = False
        print("Camera resources cleaned up.")


# Convenience function for single video recording
def record_video_for_event(event_type, duration=15, output_directory="./recordings"):
    """
    Convenience function to record a video for an event
    
    Args:
        event_type: Type of event ("motion" or "button_press")
        duration: Recording duration in seconds
        output_directory: Directory to save the video
        
    Returns:
        str: Path to recorded video or None on error
    """
    controller = CameraController(output_directory=output_directory)
    
    if not controller.initialize_camera():
        return None
    
    try:
        video_path = controller.record_video(event_type, duration=duration)
        return video_path
    finally:
        controller.cleanup()


if __name__ == "__main__":
    # Test the camera controller
    print("Testing Camera Controller...")
    print("Recording a 10 second test video...")
    
    video_path = record_video_for_event("motion", duration=10)
    
    if video_path:
        print(f"\n✓ Test successful! Video saved to: {video_path}")
    else:
        print("\n✗ Test failed!")

