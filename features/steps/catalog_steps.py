from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from features import fixture as fxt
from catalog.service import create_catalog
from catalog.api import Image
import json


# First Scenario
@given('the user has selected a list of {images}')
def selected_images(context, images):
    images = images.split(',')
    images = [Image(image.strip()) for image in images]
    context.images = images


@given('the user selected a list of detection {objects}')
def selected_objects(context, objects):
    objects = [obj.strip() for obj in objects.split(',')]
    context.objects = [dict(
        uid='1',
        objects=objects
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
    cached_catalog = await fxt.cache_client.get(catalog.uid)

    assert catalog is not None
    assert cached_catalog is not None


@then('the system creates a {number} of catalog events for each image containing the given filters')
def created_events(context, number):
    events = fxt.broker_client.get_queue('catalog')
    catalog = context.catalog
    # There can be multiple events for the same
    # catalog_uid (key)
    for key, events_in_key in events.items():
        assert key == catalog.uid
        assert len(events_in_key) == int(number)
        for event in events_in_key:
            assert 'catalog_uid' in event
            assert event['catalog_uid'] == catalog.uid


@then('the system creates a children object for the given color')
def created_children(context):
    _, event = fxt.broker_client.get_any('catalog')
    assert len(event['children']) == len(context.colors)


# Second Scenario
@given('the user selected the {scenes}')
def selected_scenes(context, scenes):
    scenes = [scn.strip() for scn in scenes.split(',')]
    context.objects = [dict(
        uid='1',
        scenes=scenes
    )]


@when('the user creates the scene filter request')
@async_run_until_complete
async def create_request(context):
    request = dict(
        images=context.images,
        scenes=context.objects
    )
    context.catalog = await create_catalog(request)


# Third Scenario
@given('the user selected a list of recognition {objects}')
def selected_objects(context, objects):
    objects = [obj.strip() for obj in objects.split(',')]
    context.objects = [dict(
        uid='1',
        objects=objects
    )]


@when('the user creates the object recognition filter request')
@async_run_until_complete
async def create_request(context):
    request = dict(
        images=context.images,
        objects=context.objects
    )
    context.catalog = await create_catalog(request)

