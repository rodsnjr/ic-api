from catalog.api import *
from uuid import uuid4

uid = '123'
colors = ['red', 'blue']
scenes = ['parking lot', 'beach']
texts = ['Text', 'Random']
objects = ['Car', 'Chair']
image_key = 'one_key'
upload_url = 'http://upload.url'


def abstract_filter():
    return ImageFilter(
        uid=uid,
        depends_on=uid
    )


def new_image() -> Image:
    return Image(
        image_key='new_image.jpg'
    )


def image() -> Image:
    return Image(
        uid=uid,
        image_key=image_key,
        upload_url=upload_url
    )


def image_without_uid() -> Image:
    return Image(
        uid=None,
        image_key=image_key,
        upload_url=None
    )


def parent_filter() -> SceneRecognition:
    return SceneRecognition(
        scenes=scenes,
        uid=uid
    )


def color_recognition() -> ColorRecognition:
    return ColorRecognition(
        colors=colors,
        uid=uid,
        depends_on=uid
    )


def color_recognition_request() -> dict:
    return dict(
        colors=colors,
        uid=uid,
        dependsOn=uid
    )


def scene_recognition() -> SceneRecognition:
    return SceneRecognition(
        scenes=scenes,
        uid=uid,
        depends_on=uid
    )


def scene_recognition_request() -> dict:
    return dict(
        scenes=scenes,
        uid=uid,
        dependsOn=uid
    )


def text_detection() -> TextDetection:
    return TextDetection(
        texts=texts,
        uid=uid,
        depends_on=uid
    )


def text_detection_request() -> dict:
    return dict(
        texts=texts,
        uid=uid,
        dependsOn=uid
    )


def object_detection(_id=uid) -> ObjectDetection:
    return ObjectDetection(
        objects=objects,
        uid=_id,
        depends_on=uid
    )


def object_detection_request(_id=uid) -> dict:
    return dict(
        objects=objects,
        uid=_id,
        dependsOn=uid
    )


def object_recognition() -> ObjectRecognition:
    return ObjectRecognition(
        objects=objects,
        uid=uid,
        depends_on=uid
    )


def object_recognition_request() -> dict:
    return dict(
        objects=objects,
        uid=uid,
        dependsOn=uid
    )


def basic_catalog() -> Catalog:
    return Catalog(
        uid=uid,
        images=[image()],
        scenes=[parent_filter()]
    )


def no_image_catalog() -> Catalog:
    return Catalog(
        uid=uid,
    )


def no_filter_catalog() -> Catalog:
    return Catalog(
        uid=uid,
        images=[image()]
    )


def no_parent_catalog() -> Catalog:
    return Catalog(
        uid=uid,
        images=[image()],
        scenes=[scene_recognition()]
    )


def multiple_parents_catalog() -> Catalog:
    return Catalog(
        uid=uid,
        images=[image()],
        scenes=[parent_filter(), parent_filter()]
    )


def catalog_request() -> dict:
    return dict(
        uid=uid,
        images=[dict(
            imageKey='1234'
        )],
        scenes=[dict(
            scenes=['beach', 'sunset']
        )]
    )


def catalog_request_with_error() -> dict:
    return dict(
        uid=uid,
        scenes=[dict(
            scenes=['beach', 'sunset']
        )]
    )


def catalog_with_children() -> Catalog:
    return Catalog(
        uid=uid,
        images=[image()],
        scenes=[parent_filter()],
        detections=[object_detection('3')],
        texts=[text_detection()],
        objects=[object_recognition()],
        colors=[ColorRecognition(colors, uid='4',
                                 depends_on='3')]
    )
