from catalog.api import *


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


def image() -> Image:
    return Image(
        image_key=image_key,
        upload_url=upload_url
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


def scene_recognition() -> SceneRecognition:
    return SceneRecognition(
        scenes=scenes,
        uid=uid,
        depends_on=uid
    )


def text_detection() -> TextDetection:
    return TextDetection(
        texts=texts,
        uid=uid,
        depends_on=uid
    )


def object_detection(_id=uid) -> ObjectDetection:
    return ObjectDetection(
        objects=objects,
        uid=_id,
        depends_on=uid
    )


def object_recognition() -> ObjectRecognition:
    return ObjectRecognition(
        objects=objects,
        uid=uid,
        depends_on=uid
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
