#!/usr/bin/env python3
"""
Test Script for Smart Doorbell System
Simulates button press or motion detection for testing purposes
"""

import time
import datetime
import sys
import os
import threading
from pymongo import MongoClient

# Import the recording and upload modules
try:
    from camera_controller import CameraController
    CAMERA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import camera_controller: {e}")
    CAMERA_AVAILABLE = False

try:
    from upload_video_to_s3 import upload_video_to_s3
    S3_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import upload_video_to_s3: {e}")
    S3_AVAILABLE = False


# --- Configuration (same as main_system.py) ---
MONGODB_CONNECTION_STRING = "mongodb+srv://doorbell:6ZbZ6ghK88CNxyQt_%40@doorbell.duv9kmk.mongodb.net/?retryWrites=true&w=majority&appName=Doorbell"
DOORBELL_ID = "12345"
RECORDINGS_DIRECTORY = "./recordings"
VIDEO_DURATION = 15
VIDEO_FPS = 10

# Global state
is_recording = False
recording_lock = threading.Lock()


def record_and_upload_video(event_type, notification_type):
    """
    Record video, upload to S3, and send notification to database
    
    Args:
        event_type: Type of event for video naming ("motion" or "button_press")
        notification_type: Type of notification for database
    """
    global is_recording
    
    with recording_lock:
        if is_recording:
            print("Already recording. Skipping this event.")
            return
        is_recording = True
    
    try:
        print(f"\n{'='*60}")
        print(f"TEST EVENT: {notification_type}")
        print(f"{'='*60}\n")
        
        # Generate recording path
        # Use local time for display, but store UTC in database
        local_now = datetime.datetime.now()
        utc_now = datetime.datetime.now(datetime.UTC)
        date_time_str = local_now.strftime("%m/%d/%y %H:%M")
        file_timestamp = local_now.strftime("%Y%m%d_%H%M%S")
        
        # Determine video filename based on event type
        if event_type.lower() == "motion":
            video_filename = f"motion_detected_{file_timestamp}.mp4"
        elif event_type.lower() == "button_press" or event_type.lower() == "doorbell":
            video_filename = f"button_pressed_{file_timestamp}.mp4"
        else:
            video_filename = f"recording_{file_timestamp}.mp4"
        
        # S3 path for database
        s3_recording_path = f"recordings/{video_filename}"
        
        # Step 1: Record video
        video_path = None
        if CAMERA_AVAILABLE:
            print("Initializing camera controller...")
            camera_controller = CameraController(output_directory=RECORDINGS_DIRECTORY)
            
            print("Starting video recording...")
            video_path = camera_controller.record_video(
                event_type=event_type,
                duration=VIDEO_DURATION,
                target_fps=VIDEO_FPS
            )
            
            if video_path:
                print(f"✓ Video recorded successfully: {video_path}")
            else:
                print("✗ Video recording failed!")
            
            # Cleanup camera resources
            camera_controller.cleanup()
        else:
            print("Camera not available. Skipping video recording.")
            print("Creating dummy video entry for testing...")
        
        # Step 2: Upload to S3 if video was recorded
        if video_path and S3_AVAILABLE:
            print("\nUploading video to S3...")
            s3_path = upload_video_to_s3(
                local_file_path=video_path,
                object_key=s3_recording_path
            )
            
            if s3_path:
                print(f"✓ Video uploaded to S3: {s3_path}")
                s3_recording_path = s3_path
            else:
                print("✗ S3 upload failed!")
        elif video_path:
            print("S3 upload not available. Video saved locally only.")
        
        # Step 3: Send notification to database
        print("\nConnecting to MongoDB...")
        try:
            client = MongoClient(MONGODB_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
            client.server_info()
            db = client["doorbells"]
            notifications_collection = db["notifications"]
            
            print("Sending notification to database...")
            
            notification_doc = {
                "notificationType": notification_type,
                "dateTime": date_time_str,
                "recordingPath": s3_recording_path,
                "doorbellID": DOORBELL_ID,
                "createdAt": utc_now
            }
           
            insert_result = notifications_collection.insert_one(notification_doc)
            print(f"✓ Notification sent to database (ID: {insert_result.inserted_id})")
            
            client.close()
        except Exception as e:
            print(f"✗ Database error: {e}")
        
        print(f"\n{'='*60}")
        print(f"TEST EVENT PROCESSING COMPLETE")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Error in record_and_upload_video: {e}")
        import traceback
        traceback.print_exc()
    finally:
        with recording_lock:
            is_recording = False


def simulate_button_press():
    """Simulate a doorbell button press"""
    print("\n" + "="*60)
    print("SIMULATING DOORBELL BUTTON PRESS")
    print("="*60 + "\n")
    
    # Start recording in a thread (like the real system)
    recording_thread = threading.Thread(
        target=record_and_upload_video,
        args=("button_press", "Doorbell Ring"),
        daemon=False  # Not daemon so we wait for completion
    )
    recording_thread.start()
    
    # Wait for recording to complete
    recording_thread.join()
    
    print("\n✓ Button press simulation complete!")


def simulate_motion_detection():
    """Simulate motion detection"""
    print("\n" + "="*60)
    print("SIMULATING MOTION DETECTION")
    print("="*60 + "\n")
    
    # Start recording in a thread (like the real system)
    recording_thread = threading.Thread(
        target=record_and_upload_video,
        args=("motion", "Motion Detected"),
        daemon=False
    )
    recording_thread.start()
    
    # Wait for recording to complete
    recording_thread.join()
    
    print("\n✓ Motion detection simulation complete!")


def main():
    """Main test function"""
    print("="*60)
    print("Smart Doorbell Test Script")
    print("="*60)
    print("\nThis script simulates doorbell events for testing.")
    print("\nAvailable tests:")
    print("  1. Simulate Button Press")
    print("  2. Simulate Motion Detection")
    print("  3. Exit")
    
    while True:
        try:
            print("\n" + "-"*60)
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                simulate_button_press()
            elif choice == "2":
                simulate_motion_detection()
            elif choice == "3":
                print("\nExiting test script. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        except KeyboardInterrupt:
            print("\n\nTest script interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["button", "doorbell", "press"]:
            simulate_button_press()
        elif arg in ["motion", "pir"]:
            simulate_motion_detection()
        else:
            print(f"Unknown argument: {arg}")
            print("Usage:")
            print("  python test_doorbell.py          # Interactive mode")
            print("  python test_doorbell.py button   # Test button press")
            print("  python test_doorbell.py motion   # Test motion detection")
    else:
        # Interactive mode
        main()

