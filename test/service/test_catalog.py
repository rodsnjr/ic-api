from catalog.service.catalog import (create_catalog, update_catalog,
                                     delete_catalog, catalog_events, find_catalog)
from .helper import upload_empty_file
from .. import fixture as fxt
from . import helper
import pytest


def assert_catalog(catalog):
    assert catalog.uid == fxt.uid
    assert len(catalog.images) == 1
    assert catalog.get_parent() is not None


def assert_events(catalog, size):
    for key, events in helper.get_events('catalog'):
        assert key == catalog.uid
        assert len(events) == size


@pytest.mark.asyncio
async def test_create_catalog():
    # Setup
    await upload_empty_file(fxt.image_key, fxt.uid)

    # Given
    basic_catalog = fxt.catalog_with_children()

    # When
    created_catalog = await create_catalog(basic_catalog)

    # Then
    assert_catalog(created_catalog)
    # Size == 1 (1 image)
    assert_events(created_catalog, 1)
    assert await helper.in_cache(created_catalog.uid)


def test_update_catalog():
    pass


def test_delete_catalog():
    pass


def test_catalog_events():
    pass


def test_find_catalog():
    pass
