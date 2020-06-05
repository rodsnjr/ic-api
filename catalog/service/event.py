from typing import Iterable
from catalog.providers import broker_client, queues
from catalog.api import CatalogEvent, CatalogEventException


async def publish_events(catalog_events: Iterable[CatalogEvent]):
    for event in catalog_events:
        await publish_event(event)


async def publish_event(catalog_event: CatalogEvent):
    try:
        await broker_client.publish(queues.catalog,
                                    key=catalog_event.catalog_uid,
                                    event=catalog_event.serialize())
    except Exception as e:
        print(e)
        raise CatalogEventException(CatalogEventException.PUBLISH_ERROR)