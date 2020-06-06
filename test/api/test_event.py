from .. import fixture as fxt
import json
import pytest


def assert_event(catalog_event, children=False):
    assert catalog_event.uid == fxt.uid
    assert catalog_event.image_key == fxt.image_key
    assert catalog_event.subject == fxt.subject
    assert catalog_event.filters == fxt.filters
    assert catalog_event.catalog_uid == fxt.uid
    if children:
        assert catalog_event.children is not None
    else:
        assert catalog_event.children is None


def assert_dict(event_dict, children=False):
    assert event_dict['uid'] == fxt.uid
    assert event_dict['image_key'] == fxt.image_key
    assert event_dict['subject'] == fxt.subject
    assert event_dict['filters'] == fxt.filters
    assert event_dict['catalog_uid'] == fxt.uid
    if children:
        assert event_dict['children'] is not None
    else:
        assert 'children' not in event_dict


def assert_child(catalog_child):
    assert catalog_child.uid == fxt.uid
    assert catalog_child.subject == fxt.subject
    assert catalog_child.filters == fxt.filters
    assert catalog_child.children is not None


def assert_child_dict(child_dict):
    assert child_dict['uid'] == fxt.uid
    assert child_dict['subject'] == fxt.subject
    assert child_dict['filters'] == fxt.filters
    assert child_dict['children'] is not None


def assert_serialized(serialized):
    deserialized = serialized.decode('utf8').replace("'", '"')
    deserialized = json.loads(deserialized)
    children = True if 'children' in deserialized else False
    assert_dict(deserialized, children=children)


def test_json_event():
    json_event = fxt.json_event()

    with pytest.raises(NotImplementedError) as err:
        json_event.serialize()

    assert json_event.ABSTRACT in str(err.value)


def test_exception():
    exception = fxt.catalog_event_exception()

    assert exception.message == fxt.CatalogEventException.PUBLISH_ERROR
    assert exception.error == fxt.CatalogEventException.ERROR


def test_catalog_event():
    catalog_event = fxt.catalog_event_with_children()

    assert_event(catalog_event, children=True)
    assert_dict(catalog_event.to_dict(), children=True)
    assert_serialized(catalog_event.serialize())


def test_catalog_event_without_children():
    catalog_event = fxt.catalog_event()
    assert_event(catalog_event)
    assert_dict(catalog_event.to_dict())
    assert_serialized(catalog_event.serialize())


def test_catalog_child():
    catalog_child = fxt.catalog_child()

    assert_child(catalog_child)
    assert_child_dict(catalog_child.to_dict())
