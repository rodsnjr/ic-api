from catalog.providers import file_client, cache_client
from catalog.api import Image
from catalog.util import generate_uid


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


async def upload_image(buffer) -> Image:
    upload_info = UploadInfo(
        buffer=buffer,
        dst_file_name=generate_uid()
    )
    upload_url = await file_client.upload_bytes(upload_info)
    image = Image(
        image_key=upload_info.dst_file_name,
        upload_url=upload_url
    )
    await cache_client.add(image.uid, image.to_dict())
    return image


async def find_image(uid: str) -> Image:
    cached_image_dict = await cache_client.get(uid)
    return Image(**cached_image_dict)


async def download_image(image_key: str):
    buffer = await file_client.download_bytes(
        download_info=DownloadInfo(
            src_file_name=image_key
        )
    )
    return buffer
