# 人脸编码接口提供
from PIL import Image
import face_recognition
from flask import Flask, request
import requests
from io import BytesIO
import json
import click

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def get_image(url_field, file_field):
    if url_field in request.form:
        return request.form[url_field], False
    else:
        return request.files[file_field].read(), True
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/face/encoding', methods=['GET', 'POST'])
def face_encoding():
    url = request.form['url']
    response = requests.get(url)
    image=face_recognition.load_image_file(BytesIO(response.content))
    face_endoings = face_recognition.face_encodings(image,model="large")
    if len(face_endoings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(url))
    if len(face_endoings) == 0:
        click.echo("WARNING: No faces found in {}. Ignoring file.".format(url))
        return json.dumps({
            'status': 'ok',
            'error': [],
            'method': '/face/encoding',
            'result': []
        })
    face_encoding = face_endoings[0].tolist()
    return json.dumps({
        'status': 'ok',
        'error': [],
        'method': '/face/encoding',
        'result': face_encoding
    })

@app.route('/face/encoding/cnn', methods=['GET', 'POST'])
def face_encoding_cnn():
    url = request.form['url']
    response = requests.get(url)
    try:
        metadata = json.loads(request.form['metadata'])
    except KeyError:
        metadata = None
    image=face_recognition.load_image_file(BytesIO(response.content))
    face_locations = face_recognition.face_locations(image,model="cnn")
    face_endoings = face_recognition.face_encodings(image,known_face_locations=face_locations,model="large")
    if len(face_endoings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(url))
    if len(face_endoings) == 0:
        click.echo("WARNING: No faces found in {}. Ignoring file.".format(url))
        return json.dumps({
            'status': 'ok',
            'error': [],
            'method': '/face/encoding',
            'result': []
        })
    face_encoding = face_endoings[0].tolist()
    return json.dumps({
        'status': 'ok',
        'error': [],
        'method': '/face/encoding/cnn',
        'result': face_encoding
    })

print('starting...')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666, debug=True)
    print('started.')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5001, debug=True)
