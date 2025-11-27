# Smart Doorbell System - Deployment Guide

This guide will help you deploy and test your smart doorbell system on Raspberry Pi 4.

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Raspberry Pi Setup](#raspberry-pi-setup)
4. [Testing the System](#testing-the-system)
5. [Web Interface](#web-interface)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

### What's New
Your smart doorbell system now has the following features:

**Frontend (Web Interface):**
- "See Recording" button in NotificationHub now links to the video player
- Video player automatically plays the recorded video from the database

**Backend (Raspberry Pi):**
- When doorbell button is pressed or motion is detected:
  1. Records a 15-second video with the Arducam
  2. Saves video locally with descriptive name (e.g., `button_pressed_20251126_143005.mp4`)
  3. Uploads video to AWS S3 bucket
  4. Creates database entry with event type and video path

**Testing:**
- New test script to simulate button press without hardware

---

## 📦 Prerequisites

### On Raspberry Pi 4:
- Python 3.7 or higher
- ffmpeg (for video encoding)
- Arducam OV2640 properly connected
- GPIO hardware (buttons, sensors, buzzer) connected

### AWS Setup:
- AWS account with S3 bucket created
- AWS credentials configured
- S3 bucket: `doorbell-video-elec290`

### MongoDB:
- MongoDB Atlas connection string configured
- Database: `doorbells`
- Collections: `notifications`, `records`

---

## 🚀 Raspberry Pi Setup

### Step 1: Transfer Files to Raspberry Pi

Transfer these folders to your Raspberry Pi:
```bash
# On your computer, use scp or any file transfer method
scp -r main/ pi@your-pi-ip:~/doorbell/
scp -r rpi4_arducam/ pi@your-pi-ip:~/doorbell/
```

### Step 2: SSH into Raspberry Pi

```bash
ssh pi@your-pi-ip
cd ~/doorbell
```

### Step 3: Install System Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install ffmpeg (required for video encoding)
sudo apt-get install ffmpeg -y

# Install Python pip if not already installed
sudo apt-get install python3-pip -y
```

### Step 4: Install Python Dependencies

```bash
# Install main system dependencies
cd ~/doorbell/main
pip3 install -r requirements.txt

# Install camera dependencies
cd ~/doorbell/rpi4_arducam
pip3 install -r requirements.txt
```

### Step 5: Configure AWS Credentials

```bash
# Install AWS CLI if not already installed
sudo apt-get install awscli -y

# Configure AWS credentials
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

### Step 6: Test Camera Setup

```bash
cd ~/doorbell/rpi4_arducam

# Test camera detection
python3 test_camera.py

# If successful, test video recording
python3 record_video.py -d 5
# This should record a 5-second test video
```

### Step 7: Verify Configuration

Edit `main/main_system.py` to verify settings:

```python
# MongoDB connection string (should already be set)
MONGODB_CONNECTION_STRING = "mongodb+srv://..."

# Doorbell ID (should match your registered doorbell)
DOORBELL_ID = "12345"

# Camera settings (adjust if needed)
VIDEO_DURATION = 15  # seconds
VIDEO_FPS = 10       # frames per second
```

---

## 🧪 Testing the System

### Option 1: Test with Test Script (No Hardware Required)

The test script simulates button press or motion detection without needing the actual hardware.

```bash
cd ~/doorbell/main

# Interactive mode - choose options from menu
python3 test_doorbell.py

# Or test button press directly
python3 test_doorbell.py button

# Or test motion detection directly
python3 test_doorbell.py motion
```

This will:
1. Record a 15-second video using the camera
2. Upload it to AWS S3
3. Create a notification in the database

**Expected Output:**
```
============================================================
TEST EVENT: Doorbell Ring
============================================================

Initializing camera controller...
Starting video recording...
Recording Video: button_press
Duration: 15 seconds
Target FPS: 10
...
✓ Video recorded successfully: ./recordings/button_pressed_20251126_143005.mp4
✓ Video uploaded to S3: recordings/button_pressed_20251126_143005.mp4
✓ Notification sent to database (ID: ...)
============================================================
TEST EVENT PROCESSING COMPLETE
============================================================
```

### Option 2: Run Full System with Hardware

```bash
cd ~/doorbell/main
python3 main_system.py
```

**Expected Output:**
```
Initializing hardware components...
Buttons initialized...
Buzzer initialized...
Motion sensors initialized...
Successfully connected to MongoDB.
Camera controller ready...
System armed. Running main loop...
```

Now press the physical doorbell button or trigger motion detection, and the system will:
1. Detect the event
2. Record video
3. Upload to S3
4. Save to database

### Option 3: Camera-Only Test

Test just the camera recording module:

```bash
cd ~/doorbell/main
python3 camera_controller.py
```

This will record a 10-second test video to verify the camera works.

---

## 🌐 Web Interface

### Starting the Server

```bash
cd server
npm install  # First time only
npm start
```

Server runs on `http://localhost:5050`

### Starting the Client

```bash
cd client
npm install  # First time only
npm start
```

Client runs on `http://localhost:3000`

### Using the Web Interface

1. **Login** to your account
2. **Navigate to Notification Hub**
3. **View notifications** - you'll see events like:
   - "Motion Detected" 
   - "Doorbell Ring"
   - "Package Delivered"
4. **Click "See Recording"** on any notification
5. **Video player** will open and automatically play the recorded video from S3

---

## 🔧 Configuration

### Adjusting Video Recording Settings

Edit `main/main_system.py`:

```python
# Change recording duration (default: 15 seconds)
VIDEO_DURATION = 15

# Change frame rate (default: 10 FPS)
# Lower FPS = smaller file size
# Higher FPS = smoother video (but slower on Pi)
VIDEO_FPS = 10
```

### Adjusting Notification Cooldowns

```python
# Prevent spam notifications (default: 60 seconds)
ULTRASONIC_NOTIFICATION_COOLDOWN = 60  # 1 minute
PIR_NOTIFICATION_COOLDOWN = 60         # 1 minute
```

### Changing S3 Bucket

Edit `main/upload_video_to_s3.py`:

```python
DEFAULT_BUCKET_NAME = "your-bucket-name-here"
```

### Changing Recordings Directory

Edit `main/main_system.py`:

```python
RECORDINGS_DIRECTORY = "./recordings"  # Change to your preferred path
```

---

## 🐛 Troubleshooting

### Camera Issues

**Problem:** Camera not detected
```bash
# Check SPI is enabled
sudo raspi-config
# Navigate to: Interface Options > SPI > Enable

# Reboot
sudo reboot

# Test camera again
cd ~/doorbell/rpi4_arducam
python3 test_camera.py
```

**Problem:** Low frame rate
- Lower the resolution in `camera_controller.py`
- Reduce VIDEO_FPS in `main_system.py`

### AWS S3 Issues

**Problem:** Upload fails - "NoCredentialsError"
```bash
# Reconfigure AWS credentials
aws configure

# Test manually
cd ~/doorbell/main
python3 upload_video_to_s3.py /path/to/test/video.mp4
```

**Problem:** Upload fails - "AccessDenied"
- Check your AWS IAM user has S3 write permissions
- Verify the bucket name is correct

### Database Issues

**Problem:** "Failed to connect to MongoDB"
- Check internet connection
- Verify MongoDB connection string is correct
- Check MongoDB Atlas IP whitelist (add 0.0.0.0/0 for testing)

### Video Player Issues

**Problem:** Video doesn't play in web interface
- Check browser console for errors
- Verify S3 bucket has public read access or proper CORS settings
- Check the S3 URL is correctly formatted

**S3 CORS Configuration:**
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

### General Issues

**Problem:** Multiple simultaneous recordings
- The system prevents this by default with a recording lock
- Only one event is processed at a time

**Problem:** System crashes or hangs
```bash
# Stop the system
# Press Ctrl+C or use emergency stop button

# Check logs for errors
# Run with Python verbose mode
python3 -u main_system.py 2>&1 | tee system.log
```

---

## 📊 File Structure

```
main/
├── main_system.py           # Main system (runs on Pi)
├── camera_controller.py     # Camera recording module (NEW)
├── upload_video_to_s3.py    # S3 upload utility (UPDATED)
├── test_doorbell.py         # Test script (NEW)
├── requirements.txt         # Python dependencies (UPDATED)
└── recordings/              # Local video storage (auto-created)

rpi4_arducam/
├── Arducam_RPI4.py         # Camera driver
├── record_video.py         # Video recording utility
├── requirements.txt        # Camera dependencies
└── ...

client/
└── src/
    └── pages/
        ├── NotificationHub.jsx  # Notification list (UPDATED)
        └── LiveVideo.jsx        # Video player (UPDATED)

server/
└── routes/
    └── notifications.js    # API endpoints
```

---

## 🎬 Quick Start Commands

```bash
# Test button press simulation
cd ~/doorbell/main
python3 test_doorbell.py button

# Run full system
cd ~/doorbell/main
python3 main_system.py

# Test camera only
cd ~/doorbell/rpi4_arducam
python3 record_video.py -d 10
```

---

## 📝 Video Naming Convention

Videos are automatically named based on the event:

- **Button Press:** `button_pressed_YYYYMMDD_HHMMSS.mp4`
- **Motion Detection:** `motion_detected_YYYYMMDD_HHMMSS.mp4`

Examples:
- `button_pressed_20251126_143005.mp4` - Button pressed on Nov 26, 2025 at 14:30:05
- `motion_detected_20251126_150030.mp4` - Motion detected on Nov 26, 2025 at 15:00:30

---

## 🔐 Security Notes

1. **MongoDB Connection String:** Contains credentials - keep it secure
2. **AWS Credentials:** Stored in `~/.aws/credentials` - keep this file secure
3. **S3 Bucket:** Configure appropriate access policies
4. **Network:** Use HTTPS for production web interface

---

## 📈 Performance Tips

1. **Lower resolution for faster recording:**
   - Edit `camera_controller.py` to use `OV2640_320x240` instead of `OV2640_640x480`

2. **Reduce video duration if storage is limited:**
   - Change `VIDEO_DURATION` to 10 or less

3. **Clean up old recordings:**
   ```bash
   # Delete recordings older than 7 days
   find ~/doorbell/main/recordings -name "*.mp4" -mtime +7 -delete
   ```

4. **Monitor disk space:**
   ```bash
   df -h
   ```

---

## ✅ System Verification Checklist

- [ ] Python dependencies installed
- [ ] ffmpeg installed
- [ ] Camera detected and working
- [ ] AWS credentials configured
- [ ] Test recording successful
- [ ] S3 upload successful
- [ ] Database connection successful
- [ ] Web interface running
- [ ] Notification appears in web interface
- [ ] Video plays in web interface

---

## 🎉 You're All Set!

Your smart doorbell system is now fully configured with:
- ✅ Automated video recording on events
- ✅ Cloud storage with AWS S3
- ✅ Web interface with video playback
- ✅ Test tools for easy debugging

For questions or issues, refer to the troubleshooting section above.

Happy monitoring! 🚪🔔📹

