import boto3, json
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

cors_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowOrigin",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{settings.bucket_name}/*"],
        }
    ],
}


cors_policy_json = json.dumps(cors_policy, indent=4)

s3_client.put_bucket_policy(Bucket=settings.bucket_name, Policy=cors_policy_json)
