# AWS S3 Video Upload Guide

This guide explains how to use the Python script to upload videos to your AWS S3 bucket.

## Prerequisites

### 1. Install Python
Make sure you have Python 3.6 or higher installed:
```bash
python --version
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

Or install boto3 directly:
```bash
pip install boto3
```

### 3. Configure AWS Credentials

You need to configure your AWS credentials. There are several ways to do this:

#### Option A: Using AWS CLI (Recommended)
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name: `us-east-1`
- Default output format: `json`

#### Option B: Using Environment Variables
```bash
# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_REGION="us-east-1"

# Linux/Mac
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_REGION="us-east-1"
```

#### Option C: Using AWS Credentials File
Create/edit `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

And `~/.aws/config`:
```ini
[default]
region = us-east-1
```

## Usage

### Basic Upload
Upload a video with its original filename:
```bash
python upload_to_s3.py path/to/your/video.mp4
```

### Upload with Custom Name
Upload a video with a custom name in S3:
```bash
python upload_to_s3.py path/to/your/video.mp4 custom_name.mp4
```

### Examples
```bash
# Upload a local video
python upload_to_s3.py doorbell_recording.mp4

# Upload with a specific name
python upload_to_s3.py recorded_video.mp4 video.mp4

# Upload from a different directory
python upload_to_s3.py C:\Videos\doorbell.mp4
```

## Supported Video Formats
- .mp4 (recommended)
- .avi
- .mov
- .mkv
- .wmv
- .flv
- .webm
- .m4v

## What Happens During Upload
1. The script validates the video file
2. Connects to AWS S3
3. Uploads the video with progress tracking
4. Sets the video to be publicly accessible
5. Provides you with the direct URL

## After Upload
Once the upload is complete, you'll receive a URL like:
```
https://doorbell-video-elec290.s3.us-east-1.amazonaws.com/video.mp4
```

This URL can be used directly in your video player!

## Troubleshooting

### Error: AWS credentials not found
- Make sure you've configured your AWS credentials (see step 3 above)
- Verify credentials are correct in AWS IAM

### Error: Access Denied
- Check that your IAM user has S3 permissions
- Required permissions: `s3:PutObject`, `s3:PutObjectAcl`

### Error: File not found
- Check the file path is correct
- Use absolute paths if relative paths don't work

### Upload is Very Slow
- Large videos take time to upload
- Check your internet connection speed
- Consider compressing the video first

## Security Notes

⚠️ **Important**: This script sets uploaded videos to be publicly accessible (`public-read` ACL). This means anyone with the URL can view the video.

If you need private videos:
1. Remove the `'ACL': 'public-read'` line from `upload_to_s3.py`
2. Configure your React app to use signed URLs for access

## Automating Uploads

### Watch a Directory (Advanced)
You can create a script to automatically upload videos from a directory:

```python
import time
import os
from upload_to_s3 import S3VideoUploader

def watch_directory(directory):
    uploader = S3VideoUploader("doorbell-video-elec290", "us-east-1")
    uploader.connect()
    
    while True:
        for file in os.listdir(directory):
            if file.endswith('.mp4'):
                file_path = os.path.join(directory, file)
                uploader.upload_video(file_path)
                os.remove(file_path)  # Remove after upload
        time.sleep(10)  # Check every 10 seconds

watch_directory("./videos_to_upload")
```

## Need Help?
- Check AWS S3 documentation: https://aws.amazon.com/s3/
- Check boto3 documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

