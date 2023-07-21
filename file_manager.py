import boto3
from dotenv import load_dotenv
import os

load_dotenv()


class FileManager:

    def __init__(self):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        self.s3_bucket_name = os.getenv("S3_BUCKET_NAME")
        self.prefix = os.getenv("INDEX_DATA_FOLDER")

        self.bucket = s3.Bucket(self.s3_bucket_name)

    def download_indexes(self):
        for obj in self.bucket.objects.filter(Prefix=self.prefix):

            if obj.key == self.prefix:
                continue

            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            self.bucket.download_file(obj.key, obj.key)

        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)

    def download_index(self, index_id):
        path = self.get_index_path(index_id)
        for obj in self.bucket.objects.filter(Prefix=path):

            if obj.key == path:
                self.bucket.download_file(obj.key, obj.key)
                print('downloaded')
                break

    def get_index_path(self, index_id):
        return f'{self.prefix}{index_id}.index'


    def upload_index(self, index_id):
        path = self.get_index_path(index_id)
        self.bucket.upload_file(path, path)
