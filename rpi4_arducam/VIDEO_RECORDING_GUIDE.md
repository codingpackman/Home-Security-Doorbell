# Video Recording Guide

Complete guide to recording videos with the Arducam OV2640 on Raspberry Pi 4.

## Overview

The OV2640 is a still camera sensor, not a video camera. However, we can record video by capturing a series of JPEG frames and compiling them into a video file. This guide covers two approaches:

1. **Real-time video recording** - Captures frames continuously and creates video with ffmpeg
2. **Time-lapse recording** - Captures frames at intervals for time-lapse photography

## Prerequisites

### Install ffmpeg (Required for Video Creation)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### Optional: Install Video Players

```bash
# VLC - versatile media player
sudo apt-get install vlc

# OMXPlayer - hardware-accelerated player for Raspberry Pi
sudo apt-get install omxplayer

# MPV - lightweight player
sudo apt-get install mpv
```

## Method 1: Real-Time Video Recording

### Basic Usage

Record a 10-second video at 10 FPS (default):

```bash
python3 record_video.py
```

This will:
1. Initialize the camera
2. Capture frames continuously
3. Save frames to a temporary folder
4. Compile frames into an MP4 video using ffmpeg
5. Clean up temporary frames
6. Output: `video_TIMESTAMP.mp4`

### Custom Duration and Frame Rate

```bash
# Record 30 seconds at 15 FPS
python3 record_video.py -d 30 --fps 15

# Record 5 seconds at 20 FPS (lower resolution recommended)
python3 record_video.py -d 5 --fps 20 -r 320x240
```

### Resolution and Frame Rate Guide

| Resolution | Realistic FPS | Notes |
|------------|---------------|-------|
| 320×240    | 15-20 FPS     | Best for action/motion |
| 640×480    | 8-12 FPS      | Good balance |
| 800×600    | 5-8 FPS       | Higher quality, slower |

**Important**: The actual frame rate depends on:
- Image resolution (lower = faster)
- Lighting conditions (bright = faster)
- Raspberry Pi performance
- SD card write speed

### Advanced Options

```bash
# Custom output filename
python3 record_video.py -o myvideo.mp4

# Keep individual frame files
python3 record_video.py --keep-frames

# Specify frames directory
python3 record_video.py --frames-dir ./my_frames

# Combine options
python3 record_video.py -d 20 --fps 12 -r 640x480 -o party.mp4
```

### Example Output

```
==============================================================
Recording Video
==============================================================
Duration: 10 seconds
Target FPS: 10
Output: video_20251125_153045.mp4
Frame storage: video_frames_20251125_153045
==============================================================

Starting recording... (press Ctrl+C to stop early)

Frame 100/100 [100.0%] | FPS: 10.2 | Capture: 85.3ms | ETA: 0.0s

==============================================================
Recording Complete
==============================================================
Frames captured: 100/100
Total time: 9.82 seconds
Average FPS: 10.18
Avg capture time: 85.3ms
Min capture time: 82.1ms
Max capture time: 98.7ms
==============================================================

Creating video from frames...
✓ Video created: video_20251125_153045.mp4
  Size: 2.45 MB
```

## Method 2: Time-Lapse Recording

Perfect for capturing slow changes over time (clouds, sunrise, construction, plant growth, etc.)

### Basic Usage

Record 60 seconds with 1 frame per second:

```bash
python3 record_timelapse.py -d 60 -i 1
```

This captures 60 frames total and saves them to `timelapse_TIMESTAMP/` folder.

### Time-Lapse Examples

```bash
# Quick time-lapse: 5 minutes, frame every 2 seconds
python3 record_timelapse.py -d 300 -i 2

# Sunrise time-lapse: 1 hour, frame every 10 seconds
python3 record_timelapse.py -d 3600 -i 10 -r 1600x1200

# Plant growth: 24 hours, frame every 5 minutes
python3 record_timelapse.py -d 86400 -i 300 -r 1024x768

# Cloud movement: 30 minutes, frame every 5 seconds
python3 record_timelapse.py -d 1800 -i 5 -r 800x600
```

### Converting Time-Lapse to Video

After recording, frames are saved in `timelapse_TIMESTAMP/`. Convert to video:

```bash
# Standard speed (30 FPS playback)
ffmpeg -framerate 30 -i timelapse_*/frame_%05d.jpg \
  -c:v libx264 -pix_fmt yuv420p timelapse.mp4

# Fast motion (60 FPS playback)
ffmpeg -framerate 60 -i timelapse_*/frame_%05d.jpg \
  -c:v libx264 -pix_fmt yuv420p timelapse_fast.mp4

# Slow motion (10 FPS playback)
ffmpeg -framerate 10 -i timelapse_*/frame_%05d.jpg \
  -c:v libx264 -pix_fmt yuv420p timelapse_slow.mp4

# Create animated GIF
ffmpeg -framerate 20 -i timelapse_*/frame_%05d.jpg timelapse.gif
```

### Time-Lapse Tips

1. **Use high resolution** - You can always downscale later
2. **Stable mounting** - Use tripod or secure mount
3. **Consistent lighting** - Best results with manual exposure
4. **Power supply** - Use wall power for long recordings
5. **SD card space** - 1600×1200 JPEG ≈ 300KB per frame

## Playing Videos

### On Raspberry Pi Desktop

```bash
# VLC (most compatible)
vlc video.mp4

# OMXPlayer (hardware accelerated)
omxplayer video.mp4

# MPV
mpv video.mp4
```

### On Another Computer

Transfer the video file and open with any video player:
- Windows: Windows Media Player, VLC
- Mac: QuickTime, VLC
- Linux: VLC, MPV, Totem

### Streaming Over Network

```bash
# Start simple HTTP server
python3 -m http.server 8000

# Access from browser: http://raspberry-pi-ip:8000
```

## Advanced ffmpeg Options

### Quality Control

```bash
# Higher quality (larger file)
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -c:v libx264 -crf 18 -pix_fmt yuv420p high_quality.mp4

# Lower quality (smaller file)
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -c:v libx264 -crf 28 -pix_fmt yuv420p low_quality.mp4
```

CRF values: 0 (lossless) to 51 (worst), 23 is default

### Resolution Scaling

```bash
# Scale to 720p
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -vf scale=1280:720 -c:v libx264 -pix_fmt yuv420p output_720p.mp4

# Scale to 1080p (upscale)
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -vf scale=1920:1080 -c:v libx264 -pix_fmt yuv420p output_1080p.mp4
```

### Add Text Overlay

```bash
# Add timestamp
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -vf "drawtext=text='%{pts\\:hms}':x=10:y=10:fontsize=24:fontcolor=white" \
  -c:v libx264 -pix_fmt yuv420p timestamped.mp4

# Add custom text
ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
  -vf "drawtext=text='My Video':x=10:y=10:fontsize=36:fontcolor=yellow" \
  -c:v libx264 -pix_fmt yuv420p titled.mp4
```

### Create Slow Motion

```bash
# Capture at high FPS, play at low FPS
python3 record_video.py -d 5 --fps 20 -r 320x240 --keep-frames

# Manually create video at 10 FPS (2x slow motion)
ffmpeg -framerate 10 -i video_frames_*/frame_%05d.jpg \
  -c:v libx264 -pix_fmt yuv420p slowmo.mp4
```

## Troubleshooting

### Low Frame Rate

**Problem**: Actual FPS much lower than target

**Solutions**:
1. Use lower resolution (`-r 320x240`)
2. Improve lighting (camera captures faster in bright light)
3. Use faster SD card (Class 10 or UHS)
4. Close other applications
5. Overclock Raspberry Pi (advanced)

### Frames Captured but No Video

**Problem**: Frames saved but ffmpeg fails

**Check**:
```bash
# Verify ffmpeg is installed
which ffmpeg

# Check frames exist
ls video_frames_*/

# Manually create video
ffmpeg -framerate 10 -i video_frames_*/frame_%05d.jpg output.mp4
```

### Choppy Video Playback

**Problem**: Video stutters during playback

**Solutions**:
1. Use hardware-accelerated player (omxplayer on RPi)
2. Lower video resolution
3. Reduce FPS
4. Use H.264 baseline profile:
   ```bash
   ffmpeg -framerate 30 -i frames/frame_%05d.jpg \
     -c:v libx264 -profile:v baseline -pix_fmt yuv420p video.mp4
   ```

### Out of Disk Space

**Problem**: Recording stops due to full SD card

**Solutions**:
1. Check available space: `df -h`
2. Delete old recordings
3. Use lower resolution
4. Save to USB drive:
   ```bash
   python3 record_video.py --frames-dir /media/usb/frames
   ```

### Recording Interrupted

**Problem**: Recording stopped unexpectedly

**Recovery**:
```bash
# Frames are still saved, create video manually
cd video_frames_TIMESTAMP
ffmpeg -framerate 10 -i frame_%05d.jpg recovered_video.mp4
```

## Performance Tips

### Optimize for Speed

1. **Use 320×240 resolution** - Fastest capture
2. **Good lighting** - Reduces exposure time
3. **Reduce target FPS** - Less CPU intensive
4. **Close background apps** - Free up resources

### Optimize for Quality

1. **Use 800×600 or higher** - Better image quality
2. **Lower FPS** - More time per frame
3. **Manual exposure settings** - Consistent brightness
4. **Stable mounting** - No motion blur

### Long-Duration Recording

For recordings over 1 hour:

1. **Use wall power** - Battery won't last
2. **Monitor temperature** - Add heatsink/cooling
3. **Check SD card space** - 1GB ≈ 3000 frames at 640×480
4. **Use time-lapse mode** - Less data, longer duration

## Real-World Examples

### Example 1: Pet Monitor

```bash
# Record 30 seconds when motion detected
python3 record_video.py -d 30 --fps 12 -o pet_activity.mp4
```

### Example 2: Garden Time-Lapse

```bash
# Capture plant growth: 8 hours, frame every 2 minutes
python3 record_timelapse.py -d 28800 -i 120 -r 1600x1200 -o garden

# Convert to 30 FPS video (240x speed)
ffmpeg -framerate 30 -i garden/frame_%05d.jpg \
  -c:v libx264 -pix_fmt yuv420p garden_timelapse.mp4
```

### Example 3: Sky/Cloud Watching

```bash
# 2 hour time-lapse, frame every 5 seconds
python3 record_timelapse.py -d 7200 -i 5 -r 1024x768 -o clouds

# Create video at 60 FPS (300x speed)
ffmpeg -framerate 60 -i clouds/frame_%05d.jpg clouds_timelapse.mp4
```

### Example 4: Traffic Monitoring

```bash
# Record 10 minutes of traffic
python3 record_video.py -d 600 --fps 10 -r 640x480 -o traffic.mp4
```

## Appendix: Frame Rate Calculations

### Real-Time Video

- **Duration**: 10 seconds
- **FPS**: 10
- **Frames**: 10 × 10 = 100 frames
- **Playback**: 10 seconds (real-time)

### Time-Lapse

- **Duration**: 3600 seconds (1 hour)
- **Interval**: 10 seconds
- **Frames**: 3600 ÷ 10 = 360 frames
- **Playback at 30 FPS**: 360 ÷ 30 = 12 seconds
- **Speed-up**: 3600 ÷ 12 = 300× faster

## Summary

| Method | Best For | Resolution | Duration | Output |
|--------|----------|------------|----------|--------|
| `record_video.py` | Real-time video | 320×240 to 800×600 | Seconds to minutes | Automatic MP4 |
| `record_timelapse.py` | Time-lapse | Any (up to 1600×1200) | Minutes to hours | Frames + Manual conversion |

**Quick Start**:
```bash
# 10-second video
python3 record_video.py

# 5-minute time-lapse  
python3 record_timelapse.py -d 300 -i 5
```

Happy recording! 🎥

