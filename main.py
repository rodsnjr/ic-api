from marshmallow import ValidationError
from quart import Quart
from quart import request, jsonify
from catalog.service import image, catalog
from catalog.api import Catalog, CatalogNotValid, catalog_schema
from catalog.api import BusinessException, ImageNotFoundException

app = Quart(__name__)


@app.route('/image', methods=['POST'])
async def create_image():
    try:
        request_json = await request.get_json()
        uploads = []
        for f in request_json['images']:
            uploaded_image = await image.upload_image(f)
            uploads.append(uploaded_image.to_dict())
        return jsonify(dict(
            images=uploads
        ))
    except Exception as e:
        print('Error creating images', e)
        return jsonify(dict(
            error='Error creating Images',
            message=str(e)
        )), 500


@app.route('/image/<uid>', methods=['GET'])
async def download_image(uid):
    try:
        found_image = await image.find_image(uid)
        download = await image.download_image(found_image.image_key)
        return download
    except ImageNotFoundException as e:
        print('Image Not Found', e)
        return jsonify(dict(
            error=e.error,
            message=str(e)
        )), 500
    except Exception as e:
        print('Error downloading image', e)
        return jsonify(dict(
            error='Error Downloading Image',
            message=str(e)
        )), 500


@app.route('/catalog', methods=['POST'])
async def create_catalog():
    try:
        request_json = await request.get_json()
        catalog_obj: Catalog = catalog_schema.load(request_json)
        catalog_created = await catalog.create_catalog(catalog_obj)
        catalog_response = catalog_schema.dump(catalog_created)
        return jsonify(catalog_response)
    except ValidationError as e:
        print('Invalid Catalog Request', e)
        return jsonify(dict(
            error='Invalid Request',
            messages=e.messages
        )), 400
    except CatalogNotValid as e:
        print('Invalid Catalog', e)
        return jsonify(dict(
            error=e.error,
            message=e.message
        )), 400
    except BusinessException as e:
        print('Business Error', e)
        return jsonify(dict(
            error=e.error,
            message=e.message
        )), 400
    except Exception as e:
        print('Error creating Catalog', e)
        return jsonify(dict(
            error='Error creating catalog',
            message=str(e)
        )), 500


@app.route('/catalog/<id>', methods=['GET'])
async def get_catalog(uid):
    try:
        catalog_found = await catalog.find_catalog(uid)
        return jsonify(catalog_schema.dumps(catalog_found))
    except Exception as e:
        print(e)
        jsonify(dict(
            error='Error Getting Catalog'
        )), 500


@app.route('/catalog/{uid}', methods=['PATCH', 'PUT'])
async def update_catalog(uid):
    try:
        catalog_obj: Catalog = catalog_schema.loads(request.body)
        catalog_found = await catalog.update_catalog(uid, catalog_obj)
        catalog_response = catalog_schema.dump(catalog_found)
        return jsonify(catalog_response)
    except ValidationError as e:
        print('Invalid Request', e)
        return jsonify(e.messages), 400
    except CatalogNotValid as e:
        print('Invalid Catalog', e)
        return jsonify(dict(
            error='Catalog Not Valid',
            message=e.message
        )), 400
    except Exception as e:
        print('Error creating Catalog', e)
        return jsonify(dict(
            error='Error creating catalog',
            message=str(e)
        )), 500


if __name__ == '__main__':
    app.run()
