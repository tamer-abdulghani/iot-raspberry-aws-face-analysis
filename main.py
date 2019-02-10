from flask import Flask, render_template, request
from os.path import isfile, join
import boto3
import json
import uuid

import os
from os import listdir
from modules import aws
from modules import camera
from modules.db import Database

app = Flask(__name__)

IMAGES = join('static', 'images')
app = Flask(__name__)
app.config['IMAGES'] = IMAGES


@app.route('/')
def menu():
    import glob
    files = glob.glob("static/images/**/*.jpg")
    return render_template('index.html', images=files)


@app.route('/train')
def train():
    if os.path.exists("static/images/tmp"):
        import shutil
        shutil.rmtree("static/images/tmp")
    return render_template('train.html')


@app.route('/train_with_aws', methods=["GET", "POST"])
def train_with_aws():
    collection = request.json['collection']
    label = request.json['label']
    all_tmp_images = [f for f in listdir("static/images/tmp") if isfile(join("static/images/tmp", f))]
    response = aws.index_faces_with_aws(all_tmp_images, collection, label)

    return json.dumps({'response': response}), 200, {'ContentType': 'application/json'}


@app.route('/access')
def access():
    if os.path.exists("static/images/tmp"):
        import shutil
        shutil.rmtree("static/images/tmp")
    return render_template('access.html')


@app.route('/screen_smile', methods=["GET", "POST"])
def screen_face():
    if not os.path.exists("static/images/tmp"):
        os.makedirs("static/images/tmp")

    unique_filename = str(uuid.uuid4()) + '.jpg'
    tmp_path = join(app.config['IMAGES'], 'tmp')
    file_path = join(tmp_path, unique_filename)

    if os.name == 'posix':
        camera.capture_picture_from_raspberry(file_path)
    else:
        camera.capture_picture_from_windows(file_path)

    resu, face_match, face_details = aws.search_faces_with_aws(file_path, 'home')

    return json.dumps({'img': file_path, 'face_match': face_match, 'face_details': face_details}), 200, {
        'ContentType': 'application/json'}


@app.route('/take_picture', methods=["GET", "POST"])
def take_picture():
    if not os.path.exists("static/images/tmp"):
        os.makedirs("static/images/tmp")

    unique_filename = str(uuid.uuid4()) + '.jpg'
    tmp_path = join(app.config['IMAGES'], 'tmp')
    file_path = join(tmp_path, unique_filename)

    if os.name == 'posix':
        camera.capture_picture_from_raspberry(file_path)
    else:
        camera.capture_picture_from_windows(file_path)

    return json.dumps({'img': file_path}), 200, {'ContentType': 'application/json'}


@app.route('/logs')
def logs():
    db = Database()
    return render_template('logs.html', logs=db.get_access_log())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
