from typing import List, Iterable
from .exception import BusinessException
from .image import Image, ImageSchema
from .filter import (ImageFilter, ObjectDetection, ObjectRecognition,
                     SceneRecognition, ColorRecognition, TextDetection)
from .filter import (SceneRecognitionSchema, ColorRecognitionSchema, ObjectDetectionSchema,
                     ObjectRecognitionSchema, TextDetectionSchema)
from marshmallow import Schema, post_load
from marshmallow import fields as f
from catalog.util import generate_uid, clean_null_terms

_ERROR_CREATING = 'Error creating Catalog'


class CatalogNotValid(BusinessException):
    NO_PARENT = 'Catalog must have a parent filter'

    NO_FILTER = 'Catalog without any filter'
    NO_IMAGE = 'Catalog without any image'
    MULTIPLE_PARENTS = 'Catalog cannot have multiple parents'

    @property
    def error(self):
        return 'Invalid Catalog'


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
        if len(parents) > 1:
            raise CatalogNotValid(CatalogNotValid.MULTIPLE_PARENTS)
        elif len(parents) == 0:
            raise CatalogNotValid(CatalogNotValid.NO_PARENT)

    def _get_parents(self):
        return filter(lambda x: x.parent_node, self.all_filters)

    def get_parent(self) -> ImageFilter:
        return next(self._get_parents())

    def get_children(self, parent: ImageFilter) -> Iterable[ImageFilter]:
        children = filter(lambda x: x.child_node, self.all_filters)
        children_of = filter(lambda x: x.depends_on is parent.uid, children)
        return children_of

    def to_dict(self) -> dict:
        return clean_null_terms(dict(
            uid=self.uid,
            images=self._to_dict_list(self.images),
            detections=self._to_dict_list(self.detections),
            objects=self._to_dict_list(self.objects),
            texts=self._to_dict_list(self.texts),
            scenes=self._to_dict_list(self.scenes),
            colors=self._to_dict_list(self.colors)
        ))


class CatalogSchema(Schema):
    uid = f.Str()
    images = f.List(f.Nested(ImageSchema), required=True)
    detections = f.List(f.Nested(ObjectDetectionSchema))
    objects = f.List(f.Nested(ObjectRecognitionSchema))
    texts = f.List(f.Nested(TextDetectionSchema))
    scenes = f.List(f.Nested(SceneRecognitionSchema))
    colors = f.List(f.Nested(ColorRecognitionSchema))

    @post_load
    def make_catalog(self, data, **kwargs):
        return Catalog(
            uid=data.get('uid', generate_uid()),
            images=data['images'],
            detections=data.get('detections', None),
            objects=data.get('objects', None),
            texts=data.get('texts', None),
            scenes=data.get('scenes', None),
            colors=data.get('colors', None)
        )

