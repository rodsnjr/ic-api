from marshmallow import Schema, post_load
from marshmallow import fields as f
from catalog.util import generate_uid, clean_null_terms
from .exception import BusinessException


class ImageNotFoundException(BusinessException):
    NOT_IN_BUCKET = 'Image not found in bucket'
    NOT_IN_CACHE = 'Image not found in Cache'

    def error(self):
        return "Image not found"


class Image:
    def __init__(self, image_key,
                 uid=generate_uid(),
                 upload_url=None):
        self.uid = uid
        self.image_key = image_key
        self.upload_url = upload_url

    def to_dict(self):
        return clean_null_terms(dict(
            uid=self.uid,
            upload_url=self.upload_url,
            image_key=self.image_key
        ))

    def __str__(self):
        return f"""
            uid={self.uid},
            image_key={self.image_key},
            upload_url={self.upload_url}
        """


class ImageSchema(Schema):
    uid = f.Str()
    image_key = f.Str(data_key='imageKey')
    upload_url = f.Str(data_key='uploadUrl')

    @post_load
    def create_image(self, data, **kwargs):
        return Image(
            uid=data.get('uid', None),
            image_key=data['image_key'],
            upload_url=data.get('upload_url', None)
        )

