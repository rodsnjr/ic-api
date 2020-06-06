import pytest
from catalog.api import CatalogEventException
from catalog.service.event import publish_event, publish_events

from .. import fixture as fxt
from . import helper


@pytest.mark.asyncio
async def test_publish_event():
    # Setup
    helper.clear()

    # Given
    event = fxt.catalog_event()

    # When
    await publish_event(event)

    # Then
    for k, events in helper.get_events('catalog'):
        assert k == fxt.uid
        assert len(events) == 1


@pytest.mark.asyncio
async def test_publish_events():
    # Setup
    helper.clear()

    # Given
    event_1 = fxt.catalog_event()
    event_2 = fxt.catalog_event_with_children()
    count_events = 0

    # When
    await publish_events((event_1, event_2,))

    # Then
    for k, events in helper.get_events('catalog'):
        assert k == fxt.uid
        count_events += len(events)

    assert count_events == 2


@pytest.mark.asyncio
async def test_publish_errors():
    # Given
    event = fxt.catalog_event()

    # When
    with helper.mock_broker_publish():
        with pytest.raises(CatalogEventException) as e:
            await publish_event(event)

    assert e.value.message == CatalogEventException.PUBLISH_ERROR
