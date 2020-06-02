import os
from catalog.providers import cache_client, broker_client, file_client


def list_images():
    return [os.path.join(PATH, 'images', img) for img in
            os.listdir(os.path.join(PATH, 'images'))]


PATH = os.path.dirname(__file__)
