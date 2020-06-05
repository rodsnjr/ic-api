from catalog.service.image import has_image, has_images, download_image, upload_image, find_image
from catalog.api import ImageNotFoundException
import pytest
from . import helper
from .. import fixture as fxt


@pytest.mark.asyncio
async def test_has_image_file():
    # Setup
    await helper.upload_empty_file(fxt.image_key, cache_id=None)

    # Given
    new_image = fxt.image_without_uid()

    # When
    has = await has_image(new_image)
    assert has


@pytest.mark.asyncio
async def test_has_images():
    # Setup
    await helper.upload_empty_file(fxt.image_key, cache_id=None)

    # Given
    new_image = fxt.image_without_uid()

    # When
    has = await has_images((new_image, ))
    assert has


@pytest.mark.asyncio
async def test_has_image_cached():
    # Setup
    await helper.upload_empty_file(fxt.image_key, cache_id=fxt.uid)

    # Given
    image = fxt.image()

    # Then
    has = await has_image(image)
    assert has


@pytest.mark.asyncio
async def test_has_image_cached_error():
    # Setup
    helper.clear()

    # Given
    image = fxt.new_image()

    # When
    with pytest.raises(ImageNotFoundException) as info:
        await has_image(image)

    assert ImageNotFoundException.NOT_IN_CACHE in info.value.message


@pytest.mark.asyncio
async def test_has_image_file_error():
    # Setup
    helper.clear()

    # Given
    image = fxt.new_image()
    image.uid = None

    # When
    with pytest.raises(ImageNotFoundException) as info:
        await has_image(image)

    assert ImageNotFoundException.NOT_IN_BUCKET in info.value.message


@pytest.mark.asyncio
async def test_find_image():
    # Setup
    await helper.upload_dummy(fxt.image_key, cache_id=fxt.uid)

    # Given
    image = fxt.image()

    # When
    found = await find_image(image.uid)

    assert found.image_key == image.image_key
    assert found.uid == image.uid


@pytest.mark.asyncio
async def test_download_image():
    # Setup
    await helper.upload_dummy(fxt.image_key, cache_id=fxt.uid)

    # Given
    image = fxt.image()

    # When
    download = await download_image(image.image_key)

    assert download is not None
    assert download == 'dummy'


@pytest.mark.asyncio
async def test_download_error():
    # Setup
    helper.clear()

    # Given
    image = fxt.image()

    with pytest.raises(ImageNotFoundException) as info:
        await download_image(image.image_key)

    assert ImageNotFoundException.NOT_IN_BUCKET in info.value.message
    assert info.value.error is not None


@pytest.mark.asyncio
async def test_upload_image():
    # Given
    buffer = '1234'

    # When
    upload = await upload_image(buffer)

    assert upload is not None
