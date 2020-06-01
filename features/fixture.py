import os
from features.providers import MockBrokerClient, MockFileClient, MockCacheClient


def list_images():
    return [os.path.join(PATH, 'images', img) for img in
            os.listdir(os.path.join(PATH, 'images'))]


PATH = os.path.dirname(__file__)
PATH_IMAGE_FILE_CLIENT = 'catalog.api.image.file_client'

PATH_IMAGE_CACHE_CLIENT = 'catalog.api.image.cache_client'
PATH_CATALOG_BROKER_CLIENT = 'catalog.event.catalog.broker_client'


PATH_CATALOG_CACHE_CLIENT = 'catalog.api.catalog.cache_client'


FILE_CLIENT = MockFileClient()
CACHE_CLIENT = MockCacheClient()
BROKER_CLIENT = MockBrokerClient()
