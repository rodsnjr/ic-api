from catalog.api import image as img


def test_image_class():
    # Given
    image_key = 'one_key'
    upload_url = 'http://upload.url'

    # When
    image_obj = img.Image(
        image_key=image_key,
        upload_url=upload_url
    )

    image_dict = image_obj.to_dict()

    # Then
    assert image_obj.image_key == image_key
    assert image_dict['image_key'] == image_key
    assert image_obj.upload_url == upload_url
    assert image_dict['upload_url'] == upload_url
    assert image_obj.id is not None
    assert image_dict['id'] == image_obj.id
