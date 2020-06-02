from typing import List


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
        return dict(
            uid=self.uid,
            depends_on=self.depends_on,
            subject=self.subject,
            filters=self.filters
        )


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
