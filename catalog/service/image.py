from typing import Iterable
from catalog.providers import file_client, cache_client
from catalog.api import Image, ImageNotFoundException
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


# FIXME has to be a batch / more eficient mode
async def has_images(images: Iterable[Image]) -> bool:
    return all([await has_image(img) for img in images])


async def has_image(image: Image) -> bool:
    # Avoid going to the file system in case you have the image id
    if image.uid is not None:
        if not await cache_client.has(key=image.uid):
            raise ImageNotFoundException(ImageNotFoundException.NOT_IN_CACHE)
    else:
        if not await file_client.has_file(image.image_key):
            raise ImageNotFoundException(ImageNotFoundException.NOT_IN_BUCKET)
    return True


async def download_image(image_key: str):
    dummy_image = Image(
        uid=None,
        image_key=image_key
    )
    if await has_image(dummy_image):
        buffer = await file_client.download_bytes(
            download_info=DownloadInfo(
                src_file_name=image_key
            )
        )
        return buffer
