"""
AWS S3 Video Upload Script
==========================
This script uploads video files to the AWS S3 bucket for the Bells Bells doorbell video project.

Prerequisites:
    - Python 3.6+
    - boto3 library: pip install boto3
    - AWS credentials configured (via AWS CLI or environment variables)

Usage:
    python upload_to_s3.py <video_file_path>
    
    Example:
    python upload_to_s3.py ./my_video.mp4
    
Environment Variables:
    AWS_ACCESS_KEY_ID     - Your AWS access key
    AWS_SECRET_ACCESS_KEY - Your AWS secret key
    AWS_REGION           - AWS region (default: us-east-1)
"""

import os
import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError

# Configuration
S3_BUCKET_NAME = "doorbell-video-elec290"
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Supported video formats
SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']


class S3VideoUploader:
    """Handles video uploads to AWS S3"""
    
    def __init__(self, bucket_name, region):
        """
        Initialize the S3 uploader
        
        Args:
            bucket_name (str): Name of the S3 bucket
            region (str): AWS region
        """
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = None
        
    def connect(self):
        """Establish connection to AWS S3"""
        try:
            self.s3_client = boto3.client('s3', region_name=self.region)
            print(f"✓ Connected to AWS S3 in region: {self.region}")
            return True
        except NoCredentialsError:
            print("✗ Error: AWS credentials not found!")
            print("\nPlease configure your AWS credentials:")
            print("  1. Using AWS CLI: aws configure")
            print("  2. Using environment variables:")
            print("     export AWS_ACCESS_KEY_ID='your_access_key'")
            print("     export AWS_SECRET_ACCESS_KEY='your_secret_key'")
            return False
        except Exception as e:
            print(f"✗ Error connecting to AWS: {str(e)}")
            return False
    
    def upload_video(self, file_path, s3_key=None):
        """
        Upload a video file to S3
        
        Args:
            file_path (str): Local path to the video file
            s3_key (str, optional): S3 object key. If None, uses the filename
            
        Returns:
            str: URL of the uploaded video, or None if upload failed
        """
        # Validate file
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"✗ Error: File not found: {file_path}")
            return None
        
        if not file_path.is_file():
            print(f"✗ Error: Not a file: {file_path}")
            return None
        
        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            print(f"✗ Error: Unsupported file format: {file_path.suffix}")
            print(f"  Supported formats: {', '.join(SUPPORTED_FORMATS)}")
            return None
        
        # Determine S3 key
        if s3_key is None:
            s3_key = file_path.name
        
        # Get file size for progress reporting
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n📤 Uploading video to S3...")
        print(f"   File: {file_path.name}")
        print(f"   Size: {file_size_mb:.2f} MB")
        print(f"   Bucket: {self.bucket_name}")
        print(f"   Key: {s3_key}")
        
        try:
            # Upload with progress callback
            self.s3_client.upload_file(
                str(file_path),
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': 'video/mp4' if file_path.suffix.lower() == '.mp4' else 'video/*',
                    'ACL': 'public-read'  # Make the video publicly accessible
                },
                Callback=ProgressPercentage(file_path)
            )
            
            # Generate the URL
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
            
            print(f"\n✓ Upload successful!")
            print(f"\n📺 Video URL:")
            print(f"   {url}")
            print(f"\n💡 You can now use this URL in your video player")
            
            return url
            
        except ClientError as e:
            print(f"\n✗ Upload failed: {str(e)}")
            return None
        except Exception as e:
            print(f"\n✗ Unexpected error: {str(e)}")
            return None


class ProgressPercentage:
    """Callback class for upload progress"""
    
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        
    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        percentage = (self._seen_so_far / self._size) * 100
        sys.stdout.write(
            f"\r   Progress: {percentage:.1f}% ({self._seen_so_far / (1024*1024):.2f} MB / {self._size / (1024*1024):.2f} MB)"
        )
        sys.stdout.flush()


def main():
    """Main function"""
    print("=" * 60)
    print("AWS S3 Video Uploader - Bells Bells Doorbell System")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n❌ Error: No video file specified")
        print("\nUsage:")
        print(f"  python {sys.argv[0]} <video_file_path>")
        print("\nExample:")
        print(f"  python {sys.argv[0]} ./doorbell_recording.mp4")
        sys.exit(1)
    
    video_file = sys.argv[1]
    
    # Optional: custom S3 key
    s3_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create uploader and upload
    uploader = S3VideoUploader(S3_BUCKET_NAME, S3_REGION)
    
    if not uploader.connect():
        sys.exit(1)
    
    url = uploader.upload_video(video_file, s3_key)
    
    if url:
        print("\n" + "=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

