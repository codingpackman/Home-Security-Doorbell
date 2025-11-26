import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


# ========= EDIT THESE 3 VALUES =========
LOCAL_FILE_PATH = r"C:\290-P1-project\aws-s3-test\video0 - Copy.mp4"  # e.g. "C:/Users/you/Videos/test.mp4"
BUCKET_NAME = "doorbell-video-elec290"                    # e.g. "my-video-bucket-123"
OBJECT_KEY = "videos1.mp4"                      # how it will be named in S3
# ======================================


def upload_video_to_s3():
    if not os.path.isfile(LOCAL_FILE_PATH):
        print(f"Error: File not found: {LOCAL_FILE_PATH}")
        return

    # Use credentials from aws configure / environment
    s3_client = boto3.client("s3")

    print(f"Uploading '{LOCAL_FILE_PATH}' to 's3://{BUCKET_NAME}/{OBJECT_KEY}' ...")

    try:
        s3_client.upload_file(
            Filename=LOCAL_FILE_PATH,
            Bucket=BUCKET_NAME,
            Key=OBJECT_KEY,
            ExtraArgs={"ContentType": "video/mp4"},
        )
    except NoCredentialsError:
        print("Error: AWS credentials not found. Did you run 'aws configure'?")
        return
    except ClientError as e:
        print("AWS ClientError occurred:")
        print(e)
        return
    except Exception as e:
        print("An unexpected error occurred:")
        print(e)
        return

    print("✅ Upload successful!")
    print(f"S3 path : s3://{BUCKET_NAME}/{OBJECT_KEY}")
    print("Example public URL (if the object is public):")
    print(f"https://{BUCKET_NAME}.s3.amazonaws.com/{OBJECT_KEY}")


if __name__ == "__main__":
    upload_video_to_s3()
