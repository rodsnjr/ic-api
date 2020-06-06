from catalog.providers import file_client, cache_client, broker_client
from catalog.service.image import UploadInfo
from unittest.mock import patch


MOCK_BROKER_PUBLISH = patch('catalog.service.event.broker_client')


def clear():
    file_client.clear()
    cache_client.clear()
    broker_client.clear()


async def upload_dummy(key, cache_id):
    await file_client.upload_bytes(UploadInfo(
        dst_file_name=key,
        buffer='dummy'
    ))
    await cache_client.add(cache_id, dict(
        uid=cache_id,
        image_key=key
    ))


async def upload_empty_file(key, cache_id=None):
    await file_client.upload_bytes(UploadInfo(
        dst_file_name=key
    ))
    if cache_id is not None:
        await cache_client.add(cache_id, dict(
            uid=cache_id,
            image_key=key
        ))


async def in_cache(key):
    return await cache_client.has(key)


async def get_from_cache(key):
    return await cache_client.get(key)


def get_events(queue):
    events = broker_client.get_queue(queue)
    for event_key, events_in_key in events.items():
        yield event_key, events_in_key
