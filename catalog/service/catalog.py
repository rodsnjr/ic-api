from typing import Iterable
from catalog.providers import cache_client
from catalog.api import (Catalog, ImageFilter,
                         CatalogEvent, CatalogChild)
from .event import publish_events
from .image import has_images


def catalog_events(catalog: Catalog) -> Iterable[CatalogEvent]:
    def _build_children(f: ImageFilter):
        return list(map(_build_child, catalog.get_children(f))) if f.parent_node else None

    def _build_child(f: ImageFilter):
        _children = _build_children(f)
        return CatalogChild(
            uid=f.uid,
            subject=f.subject,
            filters=f.filters,
            children=_children
        )

    parent = catalog.get_parent()
    children = _build_children(parent)

    for image in catalog.images:
        yield CatalogEvent(
            uid=parent.uid,
            catalog_uid=catalog.uid,
            image_key=image.image_key,
            subject=parent.subject,
            filters=parent.filters,
            children=children
        )


async def create_catalog(catalog: Catalog):
    catalog.validate()
    await has_images(catalog.images)
    await cache_client.add(catalog.uid, catalog.to_dict())
    await publish_events(catalog_events(catalog))
    return catalog


# TODO
async def update_catalog(uid: str, catalog: Catalog):
    pass


# TODO
async def delete_catalog(uid: str):
    pass


# TODO
async def find_catalog(uid: str):
    pass
