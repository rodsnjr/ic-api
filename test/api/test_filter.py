from catalog.api.filter import ColorRecognition, SceneRecognition, TextDetection
from catalog.api.filter import ObjectDetection, ObjectRecognition


def test_color_recognition():
    uid = '123'
    colors = ['red', 'blue']
    color_rec = ColorRecognition(
        colors=colors,
        uid=uid,
        depends_on=uid
    )
    color_rec_dict = color_rec.to_dict()

    assert color_rec.uid == uid
    assert color_rec_dict['uid'] == uid
    assert color_rec.depends_on == uid
    assert color_rec_dict['depends_on'] == uid
    assert color_rec.colors == colors
    assert color_rec_dict['filters'] == colors
    assert color_rec.filters == colors
    assert color_rec.subject == ColorRecognition.SUBJECT
    assert color_rec_dict['subject'] == ColorRecognition.SUBJECT
    assert not color_rec.parent_node
    assert color_rec.child_node


def test_scene_recognition():
    pass


def test_text_detection():
    pass


def test_object_detection():
    pass


def test_object_recognition():
    pass
