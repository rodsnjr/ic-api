from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from features import fixture as fxt
from features import assertions


# Upload
@given('the user has a folder of images for labeling')
def images_folder(context):
    context.images = fxt.list_images()


@given('the user selected a bunch of images in the folder')
def select_images(context):
    context.selected_images = fxt.select_random(context.images)


@when('selected the upload option')
@async_run_until_complete
async def upload_button(context):
    upload_response = await fxt.client.post('/image', json=dict(
        images=context.selected_images
    ))
    context.response = upload_response
    context.uploaded_images = await upload_response.get_json()


@then('return the information to the user')
def user_feedback(context):
    assert context.response.status_code == 200
    assert context.uploaded_images is not None


@then('the api should upload each image to the filesystem')
def uploading_images(context):
    assertions.has_uploaded(map(lambda x: x['image_key'], context.uploaded_images['images']))


@then('save the upload information to the cache')
def cache_information(context):
    assertions.has_cached(map(lambda x: x['uid'], context.uploaded_images['images']))


# Download
@given('the user has an uploaded image')
@async_run_until_complete
async def image_id(context):
    context.image = await fxt.upload_new_image('car.jpg')


@when('the user calls the system to download the given image')
@async_run_until_complete
async def start_download(context):
    download_response = await fxt.client.get(f'image/{context.image.uid}')
    context.response = download_response
    context.downloaded_image = await download_response.get_data()


@then('the api downloaded the image from the filesystem')
def downloads(context):
    assert context.response.status_code == 200
    assert context.downloaded_image is not None
