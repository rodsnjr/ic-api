from typing import List, Iterable
from catalog.providers import cache_client
from catalog.event import CatalogEvent, CatalogChild, publish_events
from .image import Image
from .filter import (ObjectDetection, ObjectRecognition,
                     SceneRecognition, ColorRecognition, TextDetection)
from uuid import uuid4

_ERROR_CREATING = 'Error creating Catalog'


def generate_uid() -> str:
    return str(uuid4())


class CatalogNotValid(Exception):
    pass


class Catalog:
    MUST_HAVE_PARENT = 'Catalog must have a parent filter'
    MULTIPLE_PARENTS = 'Catalog cannot have multiple parents'
    NO_FILTER = 'Catalog without any filter'

    @staticmethod
    def _to_dict_list(filters):
        if filters is not None:
            return list(map(lambda x: x.to_dict(), filters))

    def __init__(self,
                 uid: str = generate_uid(),
                 images: List[Image] = None,
                 detections: List[ObjectDetection] = None,
                 objects: List[ObjectRecognition] = None,
                 texts: List[TextDetection] = None,
                 scenes: List[SceneRecognition] = None,
                 colors: List[ColorRecognition] = None):
        self.uid: str = uid
        self.images: List[Image] = images
        self.detections: List[ObjectDetection] = detections
        self.texts: List[TextDetection] = texts
        self.scenes: List[SceneRecognition] = scenes
        self.objects: List[ObjectRecognition] = objects
        self.colors: List[ColorRecognition] = colors
        self._all_filters = None

    @property
    def all_filters(self):
        if self._all_filters is None:
            self._all_filters = list()
            if self.detections is not None:
                self._all_filters += self.detections
            if self.texts is not None:
                self._all_filters += self.texts
            if self.scenes is not None:
                self._all_filters += self.scenes
            if self.colors is not None:
                self._all_filters += self.colors
            if self.objects is not None:
                self._all_filters += self.objects
        return self._all_filters

    def validate(self):
        if len(self.all_filters) <= 0:
            raise CatalogNotValid(Catalog.NO_FILTER)

        parents = list(self._get_parents())
        if len(parents) <= 0:
            raise CatalogNotValid(Catalog.MUST_HAVE_PARENT)
        if len(parents) > 1:
            raise CatalogNotValid(Catalog.MULTIPLE_PARENTS)

    def _get_parents(self) -> Iterable[ImageFilter]:
        return filter(lambda x: x.parent_node, self.all_filters)

    def _get_children(self, parent: ImageFilter) -> Iterable[ImageFilter]:
        children = filter(lambda x: x.child_node, self.all_filters)
        children_of = filter(lambda x: x.depends_on is parent.uid, children)
        return children_of

    def _build_child(self, f: ImageFilter):
        children = list(map(self._build_child, self._get_children(f))) if f.parent_node else None
        return CatalogChild(
            uid=f.uid,
            subject=f.subject,
            filters=f.filters,
            children=children
        )

    def catalog_info(self) -> dict:
        return dict(
            images=self._to_dict_list(self.images),
            detections=self._to_dict_list(self.detections),
            objects=self._to_dict_list(self.objects),
            texts=self._to_dict_list(self.texts),
            scene=self._to_dict_list(self.scenes),
            colors=self._to_dict_list(self.colors)
        )

    def to_events(self) -> Iterable[CatalogEvent]:
        parent: ImageFilter = list(self._get_parents()).pop()
        children: List[CatalogChild] = list(map(self._build_child, self._get_children(parent)))

        for image in self.images:
            yield CatalogEvent(
                uid=parent.uid,
                catalog_id=self.uid,
                image_key=image.image_key,
                subject=parent.subject,
                filters=parent.filters,
                children=children
            )


def _create_object_detections(requested_detections: list) -> List[ObjectDetection]:
    if requested_detections is not None:
        return [ObjectDetection(
            labels=detection['labels'],
            uid=detection.get('uid', generate_uid()),
            depends_on=detection.get('dependsOn', None)
        ) for detection in requested_detections]


def _create_object_recognitions(request_recognitions: list) -> List[ObjectRecognition]:
    if request_recognitions is not None:
        return [
            ObjectRecognition(
                labels=recognition['labels'],
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
                labels=scene['labels'],
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


async def create_catalog(request: dict):
    catalog = Catalog(
        images=request['images'],
        detections=_create_object_detections(request.get('detections', None)),
        objects=_create_object_recognitions(request.get('objects', None)),
        texts=_create_text_detections(request.get('texts', None)),
        scenes=_create_scene_recognitions(request.get('scenes', None)),
        colors=_create_color_recognitions(request.get('colors', None))
    )
    catalog.validate()
    await cache_client.add(catalog.uid, catalog.catalog_info())
    await publish_events(catalog.to_events())
    return catalog


def update_catalog(request: dict):
    pass


def delete_catalog(request: dict):
    pass
