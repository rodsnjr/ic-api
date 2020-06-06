from typing import Iterable, List, Any
from catalog.util import clean_null_terms
import json
from .exception import BusinessException


class CatalogEventException(BusinessException):
    PUBLISH_ERROR = 'Failing to publish event'
    ERROR = "Catalog Event Error"

    @property
    def error(self):
        return self.ERROR


class JsonEvent:
    ABSTRACT = 'Abstract Method'

    def serialize(self) -> bytes:
        raise NotImplementedError(self.ABSTRACT)


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
        return clean_null_terms(dict(
            subject=self.subject,
            filters=self.filters,
            uid=self.uid,
            children=children
        ))


class CatalogEvent(JsonEvent):
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
        return clean_null_terms(dict(
            subject=self.subject,
            filters=self.filters,
            uid=self.uid,
            children=children,
            image_key=self.image_key,
            catalog_uid=self.catalog_uid
        ))

    def serialize(self) -> bytes:
        return bytes(json.dumps(self.to_dict()).encode('utf-8'))
