# Smart Doorbell - Quick Reference Card

## 🚀 Quick Start

### On Raspberry Pi:

```bash
# 1. Install dependencies (first time only)
cd ~/doorbell/main
pip3 install -r requirements.txt
sudo apt-get install ffmpeg -y

# 2. Configure AWS (first time only)
aws configure
# Enter your AWS Access Key, Secret Key, and region

# 3. Run the system
python3 main_system.py
```

---

## 🧪 Testing Commands

### Test Button Press (No Hardware)
```bash
cd ~/doorbell/main
python3 test_doorbell.py button
```

### Test Motion Detection (No Hardware)
```bash
cd ~/doorbell/main
python3 test_doorbell.py motion
```

### Interactive Test Menu
```bash
cd ~/doorbell/main
python3 test_doorbell.py
```

### Test Camera Only
```bash
cd ~/doorbell/rpi4_arducam
python3 record_video.py -d 10
```

---

## 🌐 Web Interface

### Start Server
```bash
cd server
npm start
# Runs on http://localhost:5050
```

### Start Client
```bash
cd client
npm start
# Runs on http://localhost:3000
```

### Access Notifications
1. Login at `http://localhost:3000`
2. Go to Notification Hub
3. Click "See Recording" on any notification

---

## ⚙️ Configuration

### Main Settings (`main/main_system.py`)

```python
# Video recording
VIDEO_DURATION = 15        # Change recording length (seconds)
VIDEO_FPS = 10            # Change frame rate
RECORDINGS_DIRECTORY = "./recordings"  # Change save location

# Notification cooldowns
PIR_NOTIFICATION_COOLDOWN = 60         # Motion cooldown (seconds)

# Database
DOORBELL_ID = "12345"     # Your doorbell ID
```

### AWS S3 Bucket (`main/upload_video_to_s3.py`)

```python
DEFAULT_BUCKET_NAME = "doorbell-video-elec290"
```

### Camera Resolution (`main/camera_controller.py`)

```python
# Line 19: Choose resolution
from Arducam_RPI4 import OV2640_320x240, OV2640_640x480, OV2640_800x600

# Line 128: Change default
self.resolution = OV2640_640x480  # Default
# or
self.resolution = OV2640_320x240  # Faster, smaller files
```

---

## 📹 Video File Names

Videos are automatically named:

- **Button Press:** `button_pressed_YYYYMMDD_HHMMSS.mp4`
- **Motion:** `motion_detected_YYYYMMDD_HHMMSS.mp4`

Example: `button_pressed_20251126_143005.mp4`

---

## 🗄️ Database Entry Format

```json
{
  "notificationType": "Doorbell Ring",
  "dateTime": "11/26/25 14:30",
  "recordingPath": "recordings/button_pressed_20251126_143005.mp4",
  "doorbellID": "12345",
  "createdAt": "2025-11-26T14:30:05Z"
}
```

---

## 🛠️ Troubleshooting

### Camera Not Working
```bash
# Enable SPI
sudo raspi-config
# Interface Options > SPI > Enable
sudo reboot

# Test camera
cd ~/doorbell/rpi4_arducam
python3 test_camera.py
```

### S3 Upload Fails
```bash
# Reconfigure AWS
aws configure

# Test upload
python3 upload_video_to_s3.py /path/to/video.mp4
```

### Database Connection Fails
- Check internet connection
- Verify MongoDB connection string in `main_system.py`
- Add 0.0.0.0/0 to MongoDB Atlas IP whitelist

### Video Doesn't Play
- Check S3 bucket CORS settings
- Verify bucket has public read access
- Check browser console for errors

---

## 📊 System Status Check

```bash
# Check if system is running
ps aux | grep main_system

# Check disk space
df -h

# View recent recordings
ls -lh ~/doorbell/main/recordings/

# Check Python packages
pip3 list | grep -E "boto3|pymongo|gpiozero"

# Test AWS credentials
aws s3 ls s3://doorbell-video-elec290/
```

---

## 🔄 System Workflow

```
Event → Record (15s) → Upload to S3 → Save to DB → Show in Web
```

**Timing:**
- Recording: ~15 seconds
- Upload: ~5-10 seconds (depends on network)
- Total: ~20-25 seconds per event

---

## 📦 Required Files on Raspberry Pi

```
~/doorbell/
├── main/
│   ├── main_system.py          ⭐ Main program
│   ├── camera_controller.py    ⭐ Camera control
│   ├── upload_video_to_s3.py   ⭐ S3 upload
│   ├── test_doorbell.py        ⭐ Test script
│   └── requirements.txt
└── rpi4_arducam/
    ├── Arducam_RPI4.py         ⭐ Camera driver
    ├── OV2640_reg.py
    ├── record_video.py
    └── requirements.txt
```

---

## ⌨️ Keyboard Shortcuts

### While Running main_system.py:
- **Ctrl+C** - Stop system gracefully
- **Emergency Stop Button** - Stop via hardware (if configured)

### While Testing:
- **Ctrl+C** - Interrupt test
- System waits for recording to finish before exiting

---

## 🔐 Security Checklist

- [ ] AWS credentials in `~/.aws/credentials` (not in code)
- [ ] MongoDB connection string secured
- [ ] S3 bucket has appropriate access policies
- [ ] Web interface uses HTTPS in production
- [ ] IP whitelist configured on MongoDB Atlas

---

## 📈 Performance Tips

**Faster Recording:**
- Use lower resolution: `OV2640_320x240`
- Reduce FPS: `VIDEO_FPS = 8`

**Smaller Files:**
- Lower FPS
- Lower resolution
- Shorter duration

**Less Storage:**
```bash
# Delete old recordings (7+ days)
find ~/doorbell/main/recordings -name "*.mp4" -mtime +7 -delete
```

---

## 📞 Quick Help

**System won't start?**
```bash
cd ~/doorbell/main
python3 -u main_system.py
# Look for error messages
```

**Want to test without hardware?**
```bash
python3 test_doorbell.py button
```

**Need to check if it's working?**
1. Run test script
2. Check web interface for new notification
3. Click "See Recording"
4. Video should play

---

## 📝 Common Commands Summary

```bash
# Installation
pip3 install -r requirements.txt
sudo apt-get install ffmpeg -y
aws configure

# Running
python3 main_system.py              # Run full system
python3 test_doorbell.py button     # Test button
python3 test_doorbell.py motion     # Test motion

# Testing Components
python3 camera_controller.py        # Test camera
python3 upload_video_to_s3.py file.mp4  # Test S3

# Monitoring
ps aux | grep main_system           # Check if running
ls -lh recordings/                  # View recordings
df -h                               # Check disk space
```

---

## 🎯 Expected Behavior

### When Button Pressed:
1. Buzzer rings immediately
2. Console shows "--- Doorbell Pressed ---"
3. Recording starts (takes ~15 seconds)
4. Upload to S3 (takes ~5-10 seconds)
5. Database entry created
6. Notification appears in web interface

### When Motion Detected:
1. Console shows "PIR: Motion signal received"
2. If cooldown passed, recording starts
3. Same process as button press
4. Cooldown prevents rapid re-triggering

---

## ✅ Everything Working If:

- ✅ Test script completes without errors
- ✅ Video file created in `recordings/` folder
- ✅ Video uploaded to S3 bucket
- ✅ Notification appears in database/web interface
- ✅ "See Recording" button plays the video

---

**Need more help?** See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

**Version:** 2.0  
**Last Updated:** November 26, 2025

