from marshmallow import ValidationError
from quart import Quart
from quart import request, jsonify
from catalog.service import image, catalog
from catalog.api import Catalog, CatalogNotValid, catalog_schema

app = Quart(__name__)


@app.route('/image', methods=['POST'])
async def create_image():
    try:
        uploads = []
        for f in request.files:
            uploads.append(await image.upload_image(f))
        return jsonify(dict(
            images=uploads
        ))
    except Exception as e:
        print('Error creating images', e)
        return jsonify(dict(
            error='Error creating Images',
            message=str(e)
        ))


@app.route('/image/{uid}', methods=['GET'])
async def download_image(uid):
    try:
        found_image = await image.find_image(uid)
        download = image.download_image(found_image.image_key)
        return download
    except Exception as e:
        print('Error downloading image', e)
        return jsonify(dict(
            error='Error Creating Image',
            message=str(e)
        ))


@app.route('/catalog', methods=['POST'])
async def create_catalog():
    try:
        catalog_obj: Catalog = catalog_schema.loads(request.body)
        catalog_created = await catalog.create_catalog(catalog_obj)
        return jsonify(catalog_schema.dumps(catalog_created))
    except ValidationError as e:
        print('Invalid Catalog Request', e)
        return jsonify(dict(
            error='Catalog not Valid',
            messages=e.messages
        ))
    except CatalogNotValid as e:
        print('Invalid Catalog', e)
        return jsonify(dict(
            error='Catalog Not Valid',
            message=e.message
        ))
    except Exception as e:
        print('Error creating Catalog', e)
        return jsonify(dict(
            error='Error creating catalog',
            message=str(e)
        ))


@app.route('/catalog/{id}', methods=['GET'])
async def get_catalog(uid):
    try:
        catalog_found = await catalog.find_catalog(uid)
        return jsonify(catalog_schema.dumps(catalog_found))
    except Exception as e:
        print(e)
        jsonify(dict(
            error='Error Getting Catalog'
        ))


@app.route('/catalog/{uid}', methods=['PATCH', 'PUT'])
async def update_catalog(uid):
    try:
        catalog_obj: Catalog = catalog_schema.loads(request.body)
        catalog_found = await catalog.update_catalog(uid, catalog_obj)
        return jsonify(catalog_schema.dumps(catalog_found))
    except ValidationError as e:
        print('Invalid Request', e)
        return jsonify(e.messages)
    except CatalogNotValid as e:
        print('Invalid Catalog', e)
        return jsonify(dict(
            error='Catalog Not Valid',
            message=e.message
        ))


if __name__ == '__main__':
    app.run()
