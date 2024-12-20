import boto3
import os


class S3Handler:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket,
                 local_dir="tmp"):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket = bucket
        self.local_dir = local_dir
        os.makedirs(self.local_dir, exist_ok=True)

    def list_files(self, prefixes):
        files = []
        for prefix in prefixes:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket,
                                                      Prefix=prefix)
            if 'Contents' in response:
                files.extend([obj['Key'] for obj in response['Contents']])
        return files

    def download_file(self, file_key):
        local_path = os.path.join(self.local_dir, os.path.basename(file_key))
        self.s3_client.download_file(self.bucket, file_key, local_path)
        return local_path
