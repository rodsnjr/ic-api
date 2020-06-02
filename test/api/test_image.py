from .. import fixture as fxt


def assert_image(image_obj):
    assert image_obj.image_key == fxt.image_key
    assert image_obj.upload_url == fxt.upload_url
    assert image_obj.id is not None


def assert_image_dict(image_dict, image_obj):
    assert image_dict['image_key'] == fxt.image_key
    assert image_dict['upload_url'] == fxt.upload_url
    assert image_dict['id'] == image_obj.id


def test_image_class():
    # Given
    image_obj = fxt.image()
    image_dict = image_obj.to_dict()

    # Then
    assert_image(image_obj)
    assert_image_dict(image_dict, image_obj)

