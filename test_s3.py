import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_REGION')
)

bucket = os.getenv('S3_BUCKET_NAME')
print('Bucket:', bucket)
print('Region:', os.getenv('S3_REGION'))
print('Access Key:', os.getenv('AWS_ACCESS_KEY_ID')[:10] + '...' if os.getenv('AWS_ACCESS_KEY_ID') else None)

try:
    response = s3.list_objects_v2(Bucket=bucket)
    files = [obj['Key'] for obj in response.get('Contents', [])] if 'Contents' in response else []
    print('Files in bucket:', files)
except Exception as e:
    print('Error:', str(e))
