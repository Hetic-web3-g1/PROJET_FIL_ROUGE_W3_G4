import os
import boto3
from botocore.utils import fix_s3_host

from config import settings

os.environ['AWS_ACCESS_KEY_ID'] = settings.scality_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY'] = settings.scality_secret_access_key

s3_client = boto3.client('s3', endpoint_url=f'http://{settings.s3_hostname}:{settings.s3_port}')
s3_client.meta.events.unregister('before-sign.s3', fix_s3_host)

# Create DB
s3_client.create_bucket(Bucket=settings.bucket_name)