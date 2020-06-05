import pytest
from catalog.api import CatalogNotValid, catalog_schema
from marshmallow import ValidationError
from .. import fixture as fxt


def assert_catalog(catalog):
    assert catalog.uid == fxt.uid
    assert len(catalog.images) == 1
    assert catalog.get_parent() is not None


def assert_catalog_dict(catalog_dict):
    assert catalog_dict['uid'] == fxt.uid
    assert len(catalog_dict['images']) == 1


def test_catalog():
    # Given
    catalog = fxt.basic_catalog()

    # Then
    assert_catalog(catalog)
    assert_catalog_dict(catalog.to_dict())


def test_no_parent_catalog():
    # Given
    no_parent_catalog = fxt.no_parent_catalog()

    # When
    with pytest.raises(CatalogNotValid) as info:
        no_parent_catalog.validate()

    # Then
    assert CatalogNotValid.NO_PARENT in str(info.value)


def test_no_filter_catalog():
    # Given
    no_filter_catalog = fxt.no_filter_catalog()

    # When
    with pytest.raises(CatalogNotValid) as info:
        no_filter_catalog.validate()
    # Then
    assert CatalogNotValid.NO_FILTER in str(info.value)


def test_no_image_catalog():
    # Given
    no_image_catalog = fxt.no_image_catalog()

    # When
    with pytest.raises(CatalogNotValid) as info:
        no_image_catalog.validate()
    # Then
    assert CatalogNotValid.NO_IMAGE in str(info.value)
    assert info.value.error is not None


def test_multiple_parents():
    # Given
    multiple_parent_catalog = fxt.multiple_parents_catalog()

    # When
    with pytest.raises(CatalogNotValid) as info:
        multiple_parent_catalog.validate()

    # Then
    assert CatalogNotValid.MULTIPLE_PARENTS in str(info.value)
    assert info.value.error is not None


def test_catalog_with_children():
    # Given
    catalog = fxt.catalog_with_children()

    # When
    children = catalog.get_children(catalog.get_parent())
    children = list(children)

    # Then
    assert len(children) > 1


def test_catalog_api():
    # Given
    catalog_request = fxt.catalog_request()

    # When
    catalog = catalog_schema.load(catalog_request)

    # Then
    assert_catalog(catalog)


def test_catalog_api_error():
    # Given
    catalog_request = fxt.catalog_request_with_error()

    # When
    with pytest.raises(ValidationError) as info:
        # When
        catalog_schema.load(catalog_request)

    # Then
    assert info.value.messages is not None
    assert 'images' in info.value.messages
