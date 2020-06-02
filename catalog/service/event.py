from typing import Iterable, List, Any
from catalog.providers import broker_client, queues
import json

_PUBLISH_ERROR = 'Failing to publish event'


class JSonEvent:
    def serialize(self) -> bytes:
        raise NotImplementedError('Abstract Method')


class CatalogChild:
    def __init__(self, subject: str,
                 filters: List[str],
                 uid: str,
                 children: List[Any] = None):
        self.subject: str = subject
        self.filters: List[str] = filters
        self.uid: str = uid
        self.children: List[Any] = children

    def to_dict(self):
        if self.children is not None:
            children = [c.to_dict() for c in self.children]
        else:
            children = None
        return dict(
            subject=self.subject,
            filters=self.filters,
            uid=self.uid,
            children=children
        )


class CatalogEvent(JSonEvent):
    def __init__(self, catalog_uid: str,
                 image_key: str,
                 subject: str,
                 filters: List[str],
                 uid: str,
                 children: List[CatalogChild] = None):
        self.uid: str = uid
        self.catalog_uid: str = catalog_uid
        self.image_key: str = image_key
        self.subject: str = subject
        self.filters: List[str] = filters
        self.children: List[CatalogChild] = children

    def to_dict(self):
        if self.children is not None:
            children = [c.to_dict() for c in self.children]
        else:
            children = None
        return dict(
            subject=self.subject,
            filters=self.filters,
            uid=self.uid,
            children=children,
            image_key=self.image_key,
            catalog_uid=self.catalog_uid
        )

    def serialize(self) -> bytes:
        return bytes(json.dumps(self.to_dict()).encode('utf-8'))


async def publish_events(catalog_events: Iterable[CatalogEvent]):
    try:
        for event in catalog_events:
            await publish_event(event)
    except Exception as e:
        print(e)
        raise Exception(_PUBLISH_ERROR)


async def publish_event(catalog_event: CatalogEvent):
    try:
        await broker_client.publish(queues.catalog,
                                    key=catalog_event.catalog_uid,
                                    event=catalog_event.serialize())
    except Exception as e:
        print(e)
        raise Exception(_PUBLISH_ERROR)
