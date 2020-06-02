from typing import List, Iterable
from catalog.providers import cache_client
from catalog.api import (Catalog, ImageFilter, ObjectDetection, ObjectRecognition,
                         SceneRecognition, ColorRecognition, TextDetection)
from .util import generate_uid
from .event import CatalogEvent, CatalogChild, publish_events


def _create_object_detections(requested_detections: list) -> List[ObjectDetection]:
    if requested_detections is not None:
        return [ObjectDetection(
            objects=detection['objects'],
            uid=detection.get('uid', generate_uid()),
            depends_on=detection.get('dependsOn', None)
        ) for detection in requested_detections]


def _create_object_recognitions(request_recognitions: list) -> List[ObjectRecognition]:
    if request_recognitions is not None:
        return [
            ObjectRecognition(
                objects=recognition['objects'],
                uid=recognition.get('uid', generate_uid()),
                depends_on=recognition.get('dependsOn', None)
            )
            for recognition in request_recognitions
        ]


def _create_text_detections(request_texts: list) -> List[TextDetection]:
    if request_texts is not None:
        return [
            TextDetection(
                texts=text['text'],
                uid=text.get('uid', generate_uid()),
                depends_on=text.get('dependsOn', None)
            )
            for text in request_texts
        ]


def _create_scene_recognitions(request_scenes: list) -> List[SceneRecognition]:
    if request_scenes is not None:
        return [
            SceneRecognition(
                scenes=scene['scenes'],
                uid=scene.get('uid', generate_uid()),
                depends_on=scene.get('dependsOn', None)
            )
            for scene in request_scenes
        ]


def _create_color_recognitions(request_colors: list) -> List[ColorRecognition]:
    if request_colors is not None:
        return [
            ColorRecognition(
                colors=c['colors'],
                uid=c.get('uid', generate_uid()),
                depends_on=c.get('dependsOn', None)
            )
            for c in request_colors
        ]


def _catalog_events(catalog: Catalog) -> Iterable[CatalogEvent]:
    def _build_children(f: ImageFilter):
        return list(map(_build_child, catalog.get_children(f))) if f.parent_node else None

    def _build_child(f: ImageFilter):
        _children = _build_children(f)
        return CatalogChild(
            uid=f.uid,
            subject=f.subject,
            filters=f.filters,
            children=_children
        )

    parent = catalog.get_parent()
    children = _build_children(parent)

    for image in catalog.images:
        yield CatalogEvent(
            uid=parent.uid,
            catalog_uid=catalog.uid,
            image_key=image.image_key,
            subject=parent.subject,
            filters=parent.filters,
            children=children
        )


async def create_catalog(request: dict):
    catalog = Catalog(
        uid=generate_uid(),
        images=request['images'],
        detections=_create_object_detections(request.get('detections', None)),
        objects=_create_object_recognitions(request.get('objects', None)),
        texts=_create_text_detections(request.get('texts', None)),
        scenes=_create_scene_recognitions(request.get('scenes', None)),
        colors=_create_color_recognitions(request.get('colors', None))
    )
    catalog.validate()
    await cache_client.add(catalog.uid, catalog.to_dict())
    await publish_events(_catalog_events(catalog))
    return catalog


def update_catalog(request: dict):
    pass


def delete_catalog(request: dict):
    pass
