# --- Smart Doorbell Initializer ---
# This script sets up the hardware (Doorbell Button, Sensors, Buzzer) and handles MongoDB notifications.
# Assumes you are using BCM pin numbering.

import time
import sys
import os
import datetime
import threading
from signal import pause as signal_pause
from pymongo import MongoClient

# --- AWS Configuration ---
# Set AWS credentials as environment variables
# NOTE: For production, use AWS CLI configuration or IAM roles instead

os.environ['AWS_REGION'] = 'us-east-1'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
from gpiozero import (
    Button,          # For the doorbell button
    TonalBuzzer,     # For the buzzer
    MotionSensor,    # For the PIR sensor
    DistanceSensor   # For the ultrasonic sensors
)
from gpiozero.tones import Tone

# Import camera controller and S3 upload
try:
    from camera_controller import CameraController
    CAMERA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import camera_controller: {e}")
    print("Video recording will not be available.")
    CAMERA_AVAILABLE = False

try:
    from upload_video_to_s3 import upload_video_to_s3
    S3_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import upload_video_to_s3: {e}")
    print("S3 upload will not be available.")
    S3_AVAILABLE = False

# --- 1. Hardware Pin Definitions (BCM) ---
# NOTE: We are using BCM numbering (GPIO numbers), NOT physical board numbers.
# These have been selected to avoid conflict with your SPI Camera pins (BCM 2, 3, 17, 10, 9, 11).

# Buttons
PIN_DOORBELL_BUTTON = 6  # GPIO 6

# Buzzer
PIN_BUZZER = 18           # GPIO 18

# Motion Sensors
PIN_PIR_MOTION = 27       # Physical Pin 13

# Ultrasonic Sensor 1
PIN_ULTRASONIC_1_TRIG = 23 # Physical Pin 16
PIN_ULTRASONIC_1_ECHO = 24 # Physical Pin 18

# Ultrasonic Sensor 2
PIN_ULTRASONIC_2_TRIG = 25 # Physical Pin 22
PIN_ULTRASONIC_2_ECHO = 12 # Physical Pin 32

# --- 2. Global Constants ---
running = True           # Flag to keep the main loop going

# --- MongoDB Constants ---
# !!! IMPORTANT: REPLACE WITH YOUR MONGODB ATLAS CONNECTION STRING !!!
MONGODB_CONNECTION_STRING = "mongodb+srv://username:password@doorbell.duv9kmk.mongodb.net/?retryWrites=true&w=majority&appName=Doorbell"
DOORBELL_ID = "12345"

# --- Camera Configuration ---
RECORDINGS_DIRECTORY = "./recordings"  # Directory to save recorded videos
VIDEO_DURATION = 15  # Duration of recordings in seconds
VIDEO_FPS = 3  # Target frames per second for recordings

# --- Notification Cooldowns (in seconds) ---
# Prevents sending 100 notifications if someone stands in front of the sensor
ULTRASONIC_NOTIFICATION_COOLDOWN = 60  # 1 minute
PIR_NOTIFICATION_COOLDOWN = 30         # 1 minute

# --- Cooldown Timestamps ---
last_us_notification_time = 0
last_pir_notification_time = 0

# --- Recording State ---
# Prevent multiple simultaneous recordings
is_recording = False
recording_lock = threading.Lock()


# --- 3. Hardware Initialization ---
print("Initializing hardware components...")

# Initialize hardware objects to None first
doorbell_button = None
buzzer = None
pir = None
ultrasonic1 = None
ultrasonic2 = None

# Track which hardware is available
hardware_available = {
    'buttons': False,
    'buzzer': False,
    'motion_sensors': False
}

# --- Doorbell Button ---
# Initialize button FIRST before other GPIO devices to avoid conflicts
# Using the EXACT same approach as buttontest.py which works
print(f"Attempting to initialize doorbell button on GPIO{PIN_DOORBELL_BUTTON}...")
try:
    # Initialize button the same way as buttontest.py (which works!)
    # DO NOT mess with pin factory - let gpiozero handle it automatically
    doorbell_button = Button(PIN_DOORBELL_BUTTON, pull_up=True, bounce_time=0.05)
    hardware_available['buttons'] = True
    print(f"✓ Doorbell button initialized (GPIO{PIN_DOORBELL_BUTTON})")
    print(f"  Button state: {'PRESSED' if doorbell_button.is_pressed else 'not pressed'}")
except Exception as e:
    print(f"✗ Error initializing doorbell button: {e}")
    print(f"  Error type: {type(e).__name__}")
   
    # Print full traceback for debugging
    import traceback
    print("\n  Full error details:")
    traceback.print_exc()
   
    print("\n  Troubleshooting:")
    print("  1. Make sure you run with: sudo python3 main_system.py")
    print("  2. Run: sudo python3 diagnose_gpio.py")
    print("  3. Run: sudo python3 test_button_simple.py")
    print("  4. If test_button_simple.py works but this doesn't,")
    print("     the issue is with another GPIO device initialization below")
    print("\n  Running in software-only mode (doorbell button disabled)")

# --- Buzzer ---
try:
    buzzer = TonalBuzzer(PIN_BUZZER)
    hardware_available['buzzer'] = True
    print(f"✓ Buzzer initialized (GPIO{PIN_BUZZER})")
except Exception as e:
    print(f"✗ Error initializing buzzer: {e}")
    print("  Running in software-only mode (buzzer disabled)")

# --- Motion Sensors ---
try:
    pir = MotionSensor(PIN_PIR_MOTION)
    ultrasonic1 = DistanceSensor(echo=PIN_ULTRASONIC_1_ECHO, trigger=PIN_ULTRASONIC_1_TRIG)
    ultrasonic2 = DistanceSensor(echo=PIN_ULTRASONIC_2_ECHO, trigger=PIN_ULTRASONIC_2_TRIG)
    hardware_available['motion_sensors'] = True
    print(f"✓ Motion sensors initialized.")
    print(f"  - PIR: GPIO{PIN_PIR_MOTION}")
    print(f"  - US1: Trig GPIO{PIN_ULTRASONIC_1_TRIG} / Echo GPIO{PIN_ULTRASONIC_1_ECHO}")
    print(f"  - US2: Trig GPIO{PIN_ULTRASONIC_2_TRIG} / Echo GPIO{PIN_ULTRASONIC_2_ECHO}")
except Exception as e:
    print(f"✗ Error initializing motion sensors: {e}")
    print("  Running in software-only mode (motion sensors disabled)")

# Check if any hardware is available
if not any(hardware_available.values()):
    print("\n⚠️  WARNING: No GPIO hardware initialized!")
    print("   This is normal if:")
    print("   - Running on non-Raspberry Pi hardware")
    print("   - Testing without GPIO access")
    print("   - GPIO libraries not properly installed")
    print("\n   The system will run in software-only mode.")
    print("   Use test_doorbell.py to trigger events manually.\n")


# --- MongoDB Connection ---
try:
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGODB_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
    # Test connection
    client.server_info()
    db = client["doorbells"]
    notifications_collection = db["notifications"]
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"CRITICAL: Failed to connect to MongoDB Atlas. {e}")
    print("Check connection string and network access.")
    client = None
    notifications_collection = None

# --- Camera Initialization ---
camera_controller = None
if CAMERA_AVAILABLE:
    try:
        print("Initializing camera controller...")
        camera_controller = CameraController(output_directory=RECORDINGS_DIRECTORY)
        # We'll initialize the actual camera hardware on first recording to save resources
        print("Camera controller ready (will initialize hardware on first recording).")
    except Exception as e:
        print(f"Error setting up camera controller: {e}")
        camera_controller = None
else:
    print("Camera not available. Video recording disabled.")


# --- 4. Helper Functions ---

def record_and_upload_video(event_type, notification_type):
    """
    Record video, upload to S3, and send notification to database
    This function runs in a separate thread to avoid blocking
   
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
        print(f"EVENT: {notification_type}")
        print(f"{'='*60}\n")
       
        # Generate recording path that will be used
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
       
        # S3 path for database (without bucket URL)
        s3_recording_path = f"recordings/{video_filename}"
       
        # Step 1: Record video
        video_path = None
        if camera_controller is not None:
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
        else:
            print("Camera not available. Skipping video recording.")
       
        # Step 2: Upload to S3 if video was recorded
        if video_path and S3_AVAILABLE:
            print("\nUploading video to S3...")
            s3_path = upload_video_to_s3(
                local_file_path=video_path,
                object_key=s3_recording_path
            )
           
            if s3_path:
                print(f"✓ Video uploaded to S3: {s3_path}")
                # Use the S3 path that was returned
                s3_recording_path = s3_path
            else:
                print("✗ S3 upload failed!")
        elif video_path:
            print("S3 upload not available. Video saved locally only.")
       
        # Step 3: Send notification to database
        if notifications_collection is not None:
            print("\nSending notification to database...")
           
            notification_doc = {
                "notificationType": notification_type,
                "dateTime": date_time_str,
                "recordingPath": s3_recording_path,
                "doorbellID": DOORBELL_ID,
                "createdAt": utc_now
            }
           
            insert_result = notifications_collection.insert_one(notification_doc)
            print(f"✓ Notification sent to database (ID: {insert_result.inserted_id})")
        else:
            print("Database not connected. Notification not sent.")
       
        print(f"\n{'='*60}")
        print(f"EVENT PROCESSING COMPLETE")
        print(f"{'='*60}\n")
       
    except Exception as e:
        print(f"Error in record_and_upload_video: {e}")
        import traceback
        traceback.print_exc()
    finally:
        with recording_lock:
            is_recording = False


def ring_buzzer(duration_sec=1):
    """Rings the buzzer for a specified duration."""
    if buzzer is not None:
        print("BUZZER: Ringing!")
        buzzer.play(Tone(880))
        time.sleep(duration_sec)
        buzzer.stop()
    else:
        print("BUZZER: Would ring (buzzer not available)")


# --- 5. Callback Functions (Triggered by events) ---

def doorbell_pressed_callback():
    """Called when the doorbell button is pressed."""
    print("--- Doorbell Pressed ---")
   
    # Ring the buzzer immediately for user feedback
    ring_buzzer()
   
    # Start recording and uploading in a separate thread
    # This prevents blocking the main loop
    recording_thread = threading.Thread(
        target=record_and_upload_video,
        args=("button_press", "Doorbell Ring"),
        daemon=True
    )
    recording_thread.start()

def pir_motion_detected_callback():
    """Called when the PIR sensor detects motion."""
    global last_pir_notification_time
    print("PIR: Motion signal received.")
   
    current_time = time.time()
    if (current_time - last_pir_notification_time) > PIR_NOTIFICATION_COOLDOWN:
        print("PIR: Processing motion event...")
        last_pir_notification_time = current_time
       
        # Start recording and uploading in a separate thread
        recording_thread = threading.Thread(
            target=record_and_upload_video,
            args=("motion", "Motion Detected"),
            daemon=True
        )
        recording_thread.start()
    else:
        print("PIR: Cooldown active. Event skipped.")

def pir_no_motion_callback():
    """Called when the PIR sensor stops detecting motion."""
    # print("PIR: Motion stopped.")
    pass


# --- 6. Main Program Logic ---

print("\n--- Smart Doorbell System Starting ---")
print("Assigning event handlers...")

# Assign callbacks to the hardware events
try:
    if doorbell_button is not None:
        # Assign callback just like in test_button.py
        doorbell_button.when_pressed = doorbell_pressed_callback
        print("✓ Doorbell button callback assigned")
        print(f"  Waiting for button press on GPIO{PIN_DOORBELL_BUTTON}...")
   
    if pir is not None:
        pir.when_motion = pir_motion_detected_callback
        pir.when_no_motion = pir_no_motion_callback
        print("✓ PIR motion sensor callbacks assigned")
   
    if doorbell_button is None and pir is None:
        print("\n⚠️  No hardware callbacks assigned (no GPIO hardware available)")
        print("   Use test_doorbell.py to trigger events manually")
        print("   Or press Ctrl+C to exit\n")
       
except Exception as e:
    print(f"✗ Error assigning callbacks: {e}")
    import traceback
    traceback.print_exc()


print("System armed. Running main loop... (Press Ctrl+C to exit)")

# Function to poll ultrasonic sensors in a separate thread
def ultrasonic_polling_thread():
    """Background thread to continuously poll ultrasonic sensors"""
    global last_us_notification_time, running
   
    while running:
        if ultrasonic1 is not None and ultrasonic2 is not None:
            # Ultrasonic sensors require active polling (reading the distance)
            try:
                dist1_cm = ultrasonic1.distance * 100
                dist2_cm = ultrasonic2.distance * 100
               
                # Define "close range" (e.g., less than 50cm)
                if dist1_cm < 50 or dist2_cm < 50:
                    current_time = time.time()
                   
                    # Check if cooldown has passed
                    if (current_time - last_us_notification_time) > ULTRASONIC_NOTIFICATION_COOLDOWN:
                        print(f"ULTRASONIC: Close motion detected. (S1: {dist1_cm:.1f}cm, S2: {dist2_cm:.1f}cm)")
                        last_us_notification_time = current_time
                       
                        # Start recording and uploading in a separate thread
                        recording_thread = threading.Thread(
                            target=record_and_upload_video,
                            args=("motion", "Motion Detected (Close Range)"),
                            daemon=True
                        )
                        recording_thread.start()
            except Exception as e:
                # Ignore occasional sensor reading errors
                pass
       
        # Don't poll too fast to save CPU
        time.sleep(0.5) # Check every 0.5 seconds

# Start ultrasonic polling in background thread if sensors available
if ultrasonic1 is not None and ultrasonic2 is not None:
    polling_thread = threading.Thread(target=ultrasonic_polling_thread, daemon=True)
    polling_thread.start()
    print("✓ Ultrasonic polling thread started")

try:
    # Use signal.pause() to keep the program running and allow GPIO callbacks to fire
    # This is the proper way to handle gpiozero events
    signal_pause()

except KeyboardInterrupt:
    print("\nShutdown signal received (Ctrl+C).")
    running = False

finally:
    # Clean up resources
    print("Cleaning up hardware...")
   
    # Wait for any ongoing recording to finish (max 30 seconds)
    print("Waiting for any ongoing recordings to finish...")
    wait_start = time.time()
    while is_recording and (time.time() - wait_start) < 30:
        time.sleep(1)
   
    if camera_controller is not None:
        camera_controller.cleanup()
        print("Camera resources cleaned up.")
   
    if client is not None:
        client.close()
        print("MongoDB connection closed.")
   
    if buzzer is not None:
        try:
            buzzer.stop()
            print("Buzzer turned off.")
        except:
            pass
   
    print("--- System Offline ---")
    sys.exit(0)