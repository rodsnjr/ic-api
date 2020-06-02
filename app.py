from catalog.service import image
from quart import Quart
from quart import request, jsonify

app = Quart(__name__)


@app.route('/image', methods=['GET', 'POST'])
async def image_api():
    if request.method == 'GET':
        return await image.download_image(request)
    elif request.method == 'POST':
        uploads = []
        for f in request.files:
            uploads.append(await image.upload_image(f))
        return jsonify(dict(
            images=uploads
        ))


app.run()
