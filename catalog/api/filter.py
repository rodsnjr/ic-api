from typing import List
from marshmallow import Schema, post_load
from marshmallow import fields as f
from catalog.util import generate_uid, clean_null_terms


class ImageFilter:
    ABSTRACT = 'Abstract method'

    def __init__(self, uid: str = None,
                 depends_on: str = None):
        self.uid = uid
        self.depends_on = depends_on

    @property
    def parent_node(self):
        return self.depends_on is None

    @property
    def child_node(self):
        return self.depends_on is not None

    @property
    def subject(self) -> str:
        raise NotImplementedError(ImageFilter.ABSTRACT)

    @property
    def filters(self) -> List[str]:
        raise NotImplementedError(ImageFilter.ABSTRACT)

    def to_dict(self) -> dict:
        return clean_null_terms(dict(
            uid=self.uid,
            depends_on=self.depends_on,
            subject=self.subject,
            filters=self.filters
        ))


class ColorRecognition(ImageFilter):
    SUBJECT = 'COLOR_RECOGNITION'

    def __init__(self, colors: List[str],
                 uid: str = None,
                 depends_on: str = None):
        super().__init__(uid, depends_on)
        self.colors: List[str] = colors

    @property
    def subject(self) -> str:
        return ColorRecognition.SUBJECT

    @property
    def filters(self) -> List[str]:
        return self.colors


class TextDetection(ImageFilter):
    SUBJECT = 'TEXT_DETECTION'

    def __init__(self, texts: List[str],
                 uid: str = None,
                 depends_on: str = None):
        super().__init__(uid, depends_on)
        self.texts: List[str] = texts

    @property
    def subject(self) -> str:
        return TextDetection.SUBJECT

    @property
    def filters(self) -> List[str]:
        return self.texts


class ObjectDetection(ImageFilter):
    SUBJECT = 'OBJECT_DETECTION'

    def __init__(self,
                 objects: List[str],
                 uid: str = None,
                 depends_on: str = None):
        super().__init__(uid, depends_on)
        self.objects: List[str] = objects

    @property
    def subject(self) -> str:
        return ObjectDetection.SUBJECT

    @property
    def filters(self) -> List[str]:
        return self.objects


class ObjectRecognition(ImageFilter):
    SUBJECT = 'OBJECT_RECOGNITION'

    def __init__(self, objects: List[str],
                 uid: str = None,
                 depends_on: str = None):
        super().__init__(uid, depends_on)
        self.objects: List[str] = objects

    @property
    def subject(self) -> str:
        return ObjectRecognition.SUBJECT

    @property
    def filters(self) -> List[str]:
        return self.objects


class SceneRecognition(ImageFilter):
    SUBJECT = 'SCENE_RECOGNITION'

    def __init__(self, scenes: List[str],
                 uid: str = None,
                 depends_on: str = None):
        super().__init__(uid, depends_on)
        self.scenes: List[str] = scenes

    @property
    def subject(self) -> str:
        return SceneRecognition.SUBJECT

    @property
    def filters(self) -> List[str]:
        return self.scenes


class SceneRecognitionSchema(Schema):
    uid = f.Str()
    depends_on = f.Str(data_key='dependsOn')
    scenes = f.List(f.Str(required=True))

    @post_load
    def create(self, data, **kwargs):
        return SceneRecognition(
            uid=data.get('uid', generate_uid()),
            scenes=data['scenes'],
            depends_on=data.get('depends_on', None)
        )


class ObjectRecognitionSchema(Schema):
    uid = f.Str()
    depends_on = f.Str(data_key='dependsOn')
    objects = f.List(f.Str(required=True))

    @post_load
    def create(self, data, **kwargs) -> ObjectRecognition:
        return ObjectRecognition(
            objects=data['objects'],
            uid=data.get('uid', generate_uid()),
            depends_on=data.get('depends_on', None)
        )


class ObjectDetectionSchema(Schema):
    uid = f.Str()
    depends_on = f.Str(data_key='dependsOn')
    objects = f.List(f.Str(required=True))

    @post_load
    def create(self, data, **kwargs) -> ObjectDetection:
        return ObjectDetection(
            objects=data['objects'],
            uid=data.get('uid', generate_uid()),
            depends_on=data.get('depends_on', None)
        )


class TextDetectionSchema(Schema):
    uid = f.Str()
    depends_on = f.Str(data_key='dependsOn')
    texts = f.List(f.Str(required=True))

    @post_load
    def create(self, data, **kwags):
        return TextDetection(texts=data['texts'],
                             uid=data.get('uid', generate_uid()),
                             depends_on=data.get('depends_on', None))


class ColorRecognitionSchema(Schema):
    uid = f.Str()
    depends_on = f.Str(data_key='dependsOn')
    colors = f.List(f.Str(required=True))

    @post_load
    def create(self, data, **kwargs):
        return ColorRecognition(colors=data['colors'],
                                uid=data.get('uid', generate_uid()),
                                depends_on=data.get('depends_on', None))
