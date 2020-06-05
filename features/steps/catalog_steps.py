from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from features import fixture as fxt
from features import assertions


# First Scenario
@given('the user has selected a list of {images}')
def selected_images(context, images):
    images = [image.strip() for image in images.split(',')]
    context.images = fxt.build_images(images)


@given('the user selected a list of detection {objects}')
def selected_objects(context, objects):
    objects = [obj.strip() for obj in objects.split(',')]
    context.objects = fxt.build_object_detection_request('1', objects)


@given('the user may select an {colors} filter')
def selected_color(context, colors):
    colors = [color.strip() for color in colors.split(',')]
    if len(colors) > 0:
        context.colors = fxt.build_color_recognition_request(uid='2',
                                                             depends_on='1',
                                                             colors=colors)


@when('the user creates the object detection filter request')
@async_run_until_complete
async def create_request(context):
    request = dict(
        images=context.images,
        detections=context.objects,
        colors=context.colors
    )
    response = await fxt.client.post('/catalog', json=request)
    context.response = response
    context.catalog = await response.get_json()


@then('the system should have created catalog')
@async_run_until_complete
async def created_catalog(context):
    assert context.response.status_code == 200
    context.catalog_uid = context.catalog['uid']
    assertions.has_cached([context.catalog_uid])
    assertions.has_filters(context.catalog)


@then('the system creates a {number} of catalog events for each image containing the given filters')
def created_events(context, number):
    def _events_assertion(event):
        assert 'catalog_uid' in event
        assert event['catalog_uid'] == context.catalog_uid
        if len(event['children']) > 0:
            context.children = event['children']

    assertions.has_events('catalog', key=context.catalog_uid,
                          size=number,
                          events_assertions=_events_assertion)


@then('the system creates a children object for the given color')
def created_children(context):
    assert len(context.children) == len(context.colors)


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
    response = await fxt.client.post('/catalog', json=request)
    context.response = response
    context.catalog = await response.get_json()


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
    response = await fxt.client.post('/catalog', json=request)
    context.response = response
    context.catalog = await response.get_json()

