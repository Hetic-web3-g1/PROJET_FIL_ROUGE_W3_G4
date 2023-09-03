import boto3
from botocore.utils import fix_s3_host

from config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.s3_hostname}:{settings.s3_port}",
    aws_access_key_id=settings.scality_access_key_id,
    aws_secret_access_key=settings.scality_secret_access_key,
)
s3_client.meta.events.unregister("before-sign.s3", fix_s3_host)

# Create DB
s3_client.create_bucket(Bucket=settings.bucket_name)
