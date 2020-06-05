import os
import base64
from main import app
from catalog.service import upload_image
from catalog.api import Image


PATH = os.path.dirname(__file__)
client = app.test_client()


def list_images():
    return [os.path.join(PATH, 'images', img) for img in
            os.listdir(os.path.join(PATH, 'images'))]


def build_images(images):
    return [dict(
        imageKey=image
    ) for image in images]


def build_object_detection_request(uid, objects):
    return [dict(
        uid=uid,
        objects=objects
    )]


def build_color_recognition_request(uid, depends_on, colors):
    return [dict(
            uid=uid,
            colors=colors,
            dependsOn=depends_on
    )]


async def upload_new_image(image_name):
    with open(os.path.join(PATH, 'images', image_name), 'rb') as f_bytes:
        encoded_string = base64.b64encode(f_bytes.read())
        return await upload_image(encoded_string)


def select_random(files):
    selected = []
    for file in files:
        with open(file, 'rb') as f_bytes:
            encoded_string= base64.b64encode(f_bytes.read())
            selected.append(encoded_string.decode('utf-8'))
    return selected

