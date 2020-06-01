from uuid import uuid4
from catalog.providers import file_client, cache_client
from catalog.providers import UploadInfo, DownloadInfo


class Image:
    def __init__(self, image_key,
                 upload_url=None):
        self.id = str(uuid4())
        self.image_key = image_key
        self.upload_url = upload_url

    def to_dict(self):
        return dict(
            id=self.id,
            upload_url=self.upload_url,
            image_key=self.image_key
        )


async def upload_image(buffer) -> Image:
    upload_info = UploadInfo(
        buffer=buffer,
        dst_file_name=str(uuid4())
    )
    upload_url = await file_client.upload_bytes(upload_info)
    image = Image(
        image_key=upload_info.dst_file_name,
        upload_url=upload_url
    )
    await cache_client.add(image.id, image.to_dict())
    return image


async def download_image(image_key):
    buffer = await file_client.download_bytes(
        download_info=DownloadInfo(
            src_file_name=image_key
        )
    )
    return buffer
