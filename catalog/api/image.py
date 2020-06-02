from uuid import uuid4


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

