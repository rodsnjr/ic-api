import logging
import aioboto3
from botocore.exceptions import ClientError
import io
from .config import FileConfig


# Abstract
class UploadInfo:
    def __init__(self,
                 buffer=None,
                 src_file_name=None,
                 dst_file_name=None):
        self.buffer = buffer
        self.src_file_name = src_file_name
        self.dst_file_name = dst_file_name


class DownloadInfo:
    def __init__(self,
                 src_file_name,
                 dst_file_name=None,
                 buffer=None):
        self.src_file_name = src_file_name
        self.dst_file_name = dst_file_name
        self.buffer = buffer


class FileClient:
    def __init__(self, file_config: FileConfig):
        self.config = file_config

    async def upload_file(self, upload_info: UploadInfo):
        raise NotImplementedError('Abstract Method')

    async def upload_bytes(self, upload_info: UploadInfo):
        raise NotImplementedError('Abstract Method')

    async def download_file(self, download_info: DownloadInfo):
        raise NotImplementedError('Abstract Method')

    async def download_bytes(self, download_info: DownloadInfo):
        raise NotImplementedError('Abstract Method')


# S3
class S3Client(FileClient):
    def __init__(self, file_config: FileConfig):
        super().__init__(file_config)
        self.bucket = ''

    def client(self):
        s3 = None
        try:
            url, key, secret = None, None, None
            s3 = aioboto3.client('s3',
                                 endpoint_url=url,
                                 aws_access_key_id=key,
                                 aws_secret_access_key=secret)
            return s3
        except Exception as e:
            print(e)
            raise Exception('Error on creating S3 Client')
        finally:
            if s3 is not None:
                s3.close()

    async def upload_file(self, upload_info: UploadInfo):
        # Upload the file
        try:
            with self.client() as s3_client:
                response = s3_client.upload_file(Filename=upload_info.src_file_name,
                                                 Key=upload_info.dst_file_name,
                                                 Bucket=self.bucket)
            return response
        except ClientError as e:
            logging.error(e)
            return False

    async def upload_bytes(self, upload_info: UploadInfo):
        try:
            with self.client() as s3_client:
                s3_client.put_object(Bucket=self.bucket,
                                     Key=upload_info.dst_file_name,
                                     Body=upload_info.buffer)
                return True
        except ClientError as e:
            logging.error(e)
            return False

    async def download_file(self, download_info: DownloadInfo):
        # Upload the file
        try:
            with self.client() as s3_client:
                response = s3_client.download_file(Bucket=self.bucket,
                                                   Filename=download_info.dst_file_name,
                                                   Key=download_info.src_file_name)
                return response
        except ClientError as e:
            logging.error(e)
            return False

    async def download_bytes(self, download_info: DownloadInfo):
        try:
            with self.client() as s3_client:
                obj = s3_client.get_object(Bucket=self.bucket,
                                           Key=download_info.src_file_name)
                return io.BytesIO(obj['Body'].read())
        except ClientError as e:
            logging.error(e)
            return None
