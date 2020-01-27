"""Python S3 Manager"""
import sys
import os
import boto3
from botocore.exceptions import ClientError

class s3_file_manager:

    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.client = session.client('s3')
        self.resource = session.resource('s3')
        self.bucket_name = None

    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name

    def get_file(self, file_name):
        self.check_bucket_exists()
        self.client.download_file(self.bucket_name, file_name, file_name)
        return True

    def put_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        self.check_bucket_exists()
        try:
            self.client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError:
            return False
        return True

    def check_bucket_exists(self):
        if not self.bucket_name:
            tb = sys.exc_info()[2]
            raise NameError("bucket_name not assigned").with_traceback(tb)
