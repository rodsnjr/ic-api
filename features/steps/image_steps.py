from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from features import fixture
from catalog.service import download_image, upload_image


# Upload
@given('the user has a folder of images for labeling')
def images_folder(context):
    context.images = fixture.list_images()


@given('the user selected a bunch of images in the folder')
def select_images(context):
    context.selected_images = []
    for image in context.images:
        with open(image, 'rb') as img_bytes:
            context.selected_images.append(img_bytes)


@when('selected the upload option')
@async_run_until_complete
async def upload_button(context):
    uploaded_images = []
    for image_bytes in context.selected_images:
        uploaded_images.append(await upload_image(image_bytes))
    context.uploaded_images = uploaded_images


@then('return the information to the user')
def user_feedback(context):
    assert context.uploaded_images is not None


@then('the api should upload each image to the filesystem')
def uploading_images(context):
    for image in context.uploaded_images:
        assert image.image_key in fixture.file_client.uploads


@then('save the upload information to the cache')
def cache_information(context):
    for image in context.uploaded_images:
        assert image.id in fixture.cache_client.objects


# Download
@given('the user has a image id')
def image_id(context):
    k, image_information = fixture.cache_client.objects.popitem()
    context.image_id = image_information['image_key']


@when('the user calls the system to download the given image')
@async_run_until_complete
async def start_download(context):
    img_bytes = await download_image(context.image_id)
    context.downloaded_image = img_bytes


@then('the api downloaded the image from the filesystem')
def downloads(context):
    assert context.downloaded_image is not None
