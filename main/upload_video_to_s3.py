import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


# ========= DEFAULT CONFIGURATION =========
DEFAULT_BUCKET_NAME = "doorbell-video-elec290"
# ========================================


def upload_video_to_s3(local_file_path, bucket_name=None, object_key=None):
    """
    Upload a video file to AWS S3 bucket
    
    Args:
        local_file_path: Path to the local video file
        bucket_name: S3 bucket name (default: doorbell-video-elec290)
        object_key: S3 object key/path (default: recordings/filename)
        
    Returns:
        str: S3 path to uploaded file or None on error
    """
    if bucket_name is None:
        bucket_name = DEFAULT_BUCKET_NAME
    
    if not os.path.isfile(local_file_path):
        print(f"Error: File not found: {local_file_path}")
        return None
    
    # If object_key not specified, create one based on the filename
    if object_key is None:
        filename = os.path.basename(local_file_path)
        object_key = f"recordings/{filename}"

    # Use credentials from aws configure / environment
    try:
        s3_client = boto3.client("s3")
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        return None

    print(f"Uploading '{local_file_path}' to 's3://{bucket_name}/{object_key}' ...")

    try:
        s3_client.upload_file(
            Filename=local_file_path,
            Bucket=bucket_name,
            Key=object_key,
            ExtraArgs={"ContentType": "video/mp4"},
        )
    except NoCredentialsError:
        print("Error: AWS credentials not found. Did you run 'aws configure'?")
        return None
    except ClientError as e:
        print("AWS ClientError occurred:")
        print(e)
        return None
    except Exception as e:
        print("An unexpected error occurred:")
        print(e)
        return None

    print("✅ Upload successful!")
    s3_path = f"s3://{bucket_name}/{object_key}"
    print(f"S3 path: {s3_path}")
    print("S3 URL (for database):")
    s3_url = f"{object_key}"
    print(f"  {s3_url}")
    print("Example public URL (if the object is public):")
    public_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
    print(f"  {public_url}")
    
    return s3_url  # Return the path for database storage


def main():
    """Main function for command-line usage"""
    # Example usage when run as script
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python upload_video_to_s3.py <video_file_path> [bucket_name] [object_key]")
        print("\nExample:")
        print("  python upload_video_to_s3.py /path/to/video.mp4")
        print("  python upload_video_to_s3.py /path/to/video.mp4 my-bucket recordings/video.mp4")
        sys.exit(1)
    
    local_file = sys.argv[1]
    bucket = sys.argv[2] if len(sys.argv) > 2 else None
    obj_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = upload_video_to_s3(local_file, bucket, obj_key)
    
    if result:
        print(f"\n✅ Success! S3 path: {result}")
    else:
        print("\n❌ Upload failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
