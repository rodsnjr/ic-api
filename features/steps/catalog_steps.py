from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from features import fixture as fxt
from catalog.api.catalog import create_catalog
from catalog.api.image import Image
from mock import patch


# First Scenario
@given('the user has selected a list of {images}')
def selected_images(context, images):
    images = images.split(',')
    images = [Image(image.strip()) for image in images]
    context.images = images


@given('the user selected a list of {objects}')
def selected_objects(context, objects):
    objects = [obj.strip() for obj in objects.split(',')]
    context.objects = [dict(
        uid='1',
        labels=objects
    )]


@given('the user may select an {colors} filter')
def selected_color(context, colors):
    colors = [color.strip() for color in colors.split(',')]
    if len(colors) > 0:
        context.colors = [dict(
            uid='2',
            colors=colors,
            dependsOn='1'
        )]


@when('the user creates the object detection filter request')
@async_run_until_complete
@patch(fxt.PATH_CATALOG_BROKER_CLIENT, fxt.BROKER_CLIENT)
@patch(fxt.PATH_CATALOG_CACHE_CLIENT, fxt.CACHE_CLIENT)
async def create_request(context):
    request = dict(
        images=context.images,
        detections=context.objects,
        colors=context.colors
    )
    context.catalog = await create_catalog(request)


@then('the system should have created catalog')
@async_run_until_complete
async def created_catalog(context):
    catalog = context.catalog
    cached_catalog = await fxt.CACHE_CLIENT.get(catalog.uid)

    assert catalog is not None
    assert cached_catalog is not None


@then('the system creates a {number} of catalog events for each image containing the given filters')
def created_events(context, number):
    events = fxt.BROKER_CLIENT.events['catalog']
    catalog = context.catalog

    assert len(events) == int(number)
    for event in events:
        assert event.catalog_id == catalog.uid


@then('the system creates a children object for the given color')
def created_children(context):
    events = fxt.BROKER_CLIENT.events['catalog']
    for event in events:
        assert len(event.children) == len(context.colors)


# Second Scenario
@when('the user creates the scene filter request')
@async_run_until_complete
@patch(fxt.PATH_CATALOG_BROKER_CLIENT, fxt.BROKER_CLIENT)
@patch(fxt.PATH_CATALOG_CACHE_CLIENT, fxt.CACHE_CLIENT)
async def create_request(context):
    request = dict(
        images=context.images,
        scenes=context.objects
    )
    context.catalog = await create_catalog(request)


# Third Scenario
@when('the user creates the object recognition filter request')
@async_run_until_complete
@patch(fxt.PATH_CATALOG_BROKER_CLIENT, fxt.BROKER_CLIENT)
@patch(fxt.PATH_CATALOG_CACHE_CLIENT, fxt.CACHE_CLIENT)
async def create_request(context):
    request = dict(
        images=context.images,
        objects=context.objects
    )
    context.catalog = await create_catalog(request)

