import pytest
from catalog.api.filter import (ColorRecognitionSchema, ObjectRecognitionSchema,
                                TextDetectionSchema, ObjectDetectionSchema,
                                SceneRecognitionSchema)
from .. import fixture as fxt


def assert_filter(filter_obj, uid, filters, subject, depends_on=None):
    assert filter_obj.uid == uid
    assert filter_obj.depends_on == depends_on
    assert filter_obj.filters == filters
    assert filter_obj.subject == subject
    if depends_on is not None:
        assert not filter_obj.parent_node
        assert filter_obj.child_node
    else:
        assert filter_obj.parent_node
        assert not filter_obj.child_node


def assert_filter_dict(filter_dict, uid, filters, subject, depends_on=None):
    assert filter_dict['uid'] == uid, f'dict should have uid[{uid}]'
    assert filter_dict['depends_on'] == depends_on, f'dict should have depends_on [{depends_on}]'
    assert filter_dict['filters'] == filters, f'dict filters should have [{filters}]'
    assert filter_dict['subject'] == subject, f'dict subject should have [{subject}]'


def test_abstract_filter():
    abstract_filter = fxt.abstract_filter()

    assert abstract_filter.uid == fxt.uid
    assert abstract_filter.depends_on == fxt.uid
    assert abstract_filter.child_node
    assert not abstract_filter.parent_node

    with pytest.raises(NotImplementedError) as e:
        assert abstract_filter.subject is None

    assert abstract_filter.ABSTRACT in str(e.value)

    with pytest.raises(NotImplementedError) as e:
        assert abstract_filter.filters is None

    assert abstract_filter.ABSTRACT in str(e.value)


def test_parent_filter():
    # Given
    color_rec = fxt.color_recognition()

    color_rec.depends_on = None

    assert_filter(color_rec, fxt.uid, fxt.colors,
                  color_rec.SUBJECT)

    assert_filter_dict(color_rec.to_dict(), fxt.uid,
                       fxt.colors, color_rec.SUBJECT)


def test_color_recognition():
    # Given
    color_rec = fxt.color_recognition()

    # Then
    assert color_rec.colors == fxt.colors

    assert_filter(color_rec, fxt.uid, fxt.colors,
                  color_rec.SUBJECT,
                  depends_on=fxt.uid)

    assert_filter_dict(color_rec.to_dict(), fxt.uid,
                       fxt.colors, color_rec.SUBJECT,
                       depends_on=fxt.uid)


def test_color_recognition_schema():
    # Given
    color_rec_request = fxt.color_recognition_request()
    schema = ColorRecognitionSchema()

    # When
    color_rec = schema.load(color_rec_request)

    # Then
    assert_filter(color_rec, fxt.uid, fxt.colors,
                  color_rec.SUBJECT,
                  depends_on=fxt.uid)


def test_scene_recognition():
    # Given
    scene_rec = fxt.scene_recognition()

    # Then
    assert scene_rec.scenes == fxt.scenes

    assert_filter(scene_rec, fxt.uid, fxt.scenes,
                  scene_rec.SUBJECT,
                  depends_on=fxt.uid)

    assert_filter_dict(scene_rec.to_dict(), fxt.uid,
                       fxt.scenes, scene_rec.SUBJECT,
                       depends_on=fxt.uid)


def test_scene_recognition_schema():
    # Given
    scene_rec_request = fxt.scene_recognition_request()
    schema = SceneRecognitionSchema()

    # When
    scene_rec = schema.load(scene_rec_request)

    # Then
    assert_filter(scene_rec, fxt.uid, fxt.scenes,
                  scene_rec.SUBJECT,
                  depends_on=fxt.uid)


def test_text_detection():
    # Given
    text_det = fxt.text_detection()

    # Then
    assert text_det.texts == fxt.texts

    assert_filter(text_det, fxt.uid, fxt.texts,
                  text_det.SUBJECT,
                  depends_on=fxt.uid)

    assert_filter_dict(text_det.to_dict(), fxt.uid,
                       fxt.texts, text_det.SUBJECT,
                       depends_on=fxt.uid)


def test_text_detection_schema():
    # Given
    text_det_request = fxt.text_detection_request()
    schema = TextDetectionSchema()

    # When
    text_det = schema.load(text_det_request)

    # Then
    assert_filter(text_det, fxt.uid, fxt.texts,
                  text_det.SUBJECT,
                  depends_on=fxt.uid)


def test_object_detection():
    # Given
    object_det = fxt.object_detection()

    # Then
    assert object_det.objects == fxt.objects

    assert_filter(object_det, fxt.uid, fxt.objects,
                  object_det.SUBJECT,
                  depends_on=fxt.uid)

    assert_filter_dict(object_det.to_dict(), fxt.uid,
                       fxt.objects, object_det.SUBJECT,
                       depends_on=fxt.uid)


def test_object_detection_schema():
    # Given
    object_det_request = fxt.object_detection_request()
    schema = ObjectDetectionSchema()

    # When
    object_det = schema.load(object_det_request)

    # Then
    assert object_det.objects == fxt.objects
    assert_filter(object_det, fxt.uid, fxt.objects,
                  object_det.SUBJECT,
                  depends_on=fxt.uid)


def test_object_recognition():
    # Given
    object_rec = fxt.object_recognition()

    # Then
    assert object_rec.objects == fxt.objects

    assert_filter(object_rec, fxt.uid, fxt.objects,
                  object_rec.SUBJECT,
                  depends_on=fxt.uid)

    assert_filter_dict(object_rec.to_dict(), fxt.uid,
                       fxt.objects, object_rec.SUBJECT,
                       depends_on=fxt.uid)


def test_object_recognition_schema():
    # Given
    object_rec_request = fxt.object_recognition_request()
    schema = ObjectRecognitionSchema()

    # When
    object_rec = schema.load(object_rec_request)

    # Then
    assert object_rec.objects == fxt.objects
    assert_filter(object_rec, fxt.uid, fxt.objects,
                  object_rec.SUBJECT,
                  depends_on=fxt.uid)