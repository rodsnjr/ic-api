from typing import List, Iterable
from .image import Image
from .filter import (ImageFilter, ObjectDetection, ObjectRecognition,
                     SceneRecognition, ColorRecognition, TextDetection)
from .filter import (SceneRecognitionSchema, ColorRecognitionSchema, ObjectDetectionSchema,
                     ObjectRecognitionSchema, TextDetectionSchema)
from marshmallow import Schema, fields, post_load
from catalog.util import generate_uid

_ERROR_CREATING = 'Error creating Catalog'


class CatalogNotValid(Exception):
    NO_PARENT = 'Catalog must have a parent filter'
    NO_FILTER = 'Catalog without any filter'
    NO_IMAGE = 'Catalog without any image'
    MULTIPLE_PARENTS = 'Catalog cannot have multiple parents'

    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class Catalog:
    @staticmethod
    def _to_dict_list(filters):
        if filters is not None:
            return list(map(lambda x: x.to_dict(), filters))

    def __init__(self,
                 uid: str = None,
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
        if self.images is None or len(self.images) <= 0:
            raise CatalogNotValid(CatalogNotValid.NO_IMAGE)

        if len(self.all_filters) <= 0:
            raise CatalogNotValid(CatalogNotValid.NO_FILTER)

        parents = list(self._get_parents())
        if len(parents) <= 0:
            raise CatalogNotValid(CatalogNotValid.NO_PARENT)
        if len(parents) > 1:
            raise CatalogNotValid(CatalogNotValid.MULTIPLE_PARENTS)

    def _get_parents(self):
        return filter(lambda x: x.parent_node, self.all_filters)

    def get_parent(self) -> ImageFilter:
        return next(self._get_parents())

    def get_children(self, parent: ImageFilter) -> Iterable[ImageFilter]:
        children = filter(lambda x: x.child_node, self.all_filters)
        children_of = filter(lambda x: x.depends_on is parent.uid, children)
        return children_of

    def to_dict(self) -> dict:
        return dict(
            uid=self.uid,
            images=self._to_dict_list(self.images),
            detections=self._to_dict_list(self.detections),
            objects=self._to_dict_list(self.objects),
            texts=self._to_dict_list(self.texts),
            scenes=self._to_dict_list(self.scenes),
            colors=self._to_dict_list(self.colors)
        )


class CatalogSchema(Schema):
    uid = fields.Str()
    images = fields.Str()
    detections = fields.Nested(ObjectDetectionSchema)
    objects = fields.Nested(ObjectRecognitionSchema)
    texts = fields.Nested(TextDetectionSchema)
    scenes = fields.Nested(SceneRecognitionSchema)
    colors = fields.Nested(ColorRecognitionSchema)

    def _create_object_detections(self, requested_detections: list) -> List[ObjectDetection]:
        if requested_detections is not None:
            return [ObjectDetection(
                objects=detection['objects'],
                uid=detection.get('uid', generate_uid()),
                depends_on=detection.get('dependsOn', None)
            ) for detection in requested_detections]

    def _create_object_recognitions(self, request_recognitions: list) -> List[ObjectRecognition]:
        if request_recognitions is not None:
            return [
                ObjectRecognition(
                    objects=recognition['objects'],
                    uid=recognition.get('uid', generate_uid()),
                    depends_on=recognition.get('dependsOn', None)
                )
                for recognition in request_recognitions
            ]

    def _create_text_detections(self, request_texts: list) -> List[TextDetection]:
        if request_texts is not None:
            return [
                TextDetection(
                    texts=text['text'],
                    uid=text.get('uid', generate_uid()),
                    depends_on=text.get('dependsOn', None)
                )
                for text in request_texts
            ]

    def _create_scene_recognitions(self, request_scenes: list) -> List[SceneRecognition]:
        if request_scenes is not None:
            return [
                SceneRecognition(
                    scenes=scene['scenes'],
                    uid=scene.get('uid', generate_uid()),
                    depends_on=scene.get('dependsOn', None)
                )
                for scene in request_scenes
            ]

    def _create_color_recognitions(self, request_colors: list) -> List[ColorRecognition]:
        if request_colors is not None:
            return [
                ColorRecognition(
                    colors=c['colors'],
                    uid=c.get('uid', generate_uid()),
                    depends_on=c.get('dependsOn', None)
                )
                for c in request_colors
            ]

    @post_load
    def make_catalog(self, data, **kwargs):
        return Catalog(
            uid=generate_uid(),
            images=data['images'],
            detections=self._create_object_detections(data.get('detections', None)),
            objects=self._create_object_recognitions(data.get('objects', None)),
            texts=self._create_text_detections(data.get('texts', None)),
            scenes=self._create_scene_recognitions(data.get('scenes', None)),
            colors=self._create_color_recognitions(data.get('colors', None))
        )
