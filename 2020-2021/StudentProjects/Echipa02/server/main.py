import os

import face_recognition
from PIL import Image
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS, cross_origin
import pickle
from luxand import luxand
from datetime import datetime

import numpy as np
import keras
from keras.models import load_model
import cv2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img = Image.open(file).copy()

            received_image_encodings = face_recognition.face_encodings(face_recognition.load_image_file(file))

            if len(received_image_encodings) == 0:
                return jsonify("no face was found")

            encoding = received_image_encodings[0]
            analysys_result = analyze_image(encoding)

            if analysys_result['action'] == 'log in':
                return jsonify(analysys_result)
            else:
                img.save('./user_pictures/' + analysys_result['new_img_name'] + '.png', 'PNG')
                pickle.dump(encoding, open('./user_encodings/' + analysys_result['new_img_name'] + '.p', 'wb'))
                return jsonify(analysys_result)

    if request.method == 'GET':
        return '''
            <!doctype html>
            <title>Is this a picture of a kid?</title>
            <h1>Login/register with your picture</h1>
            <form method="POST" enctype="multipart/form-data">
              <input type="file" name="file">
              <input type="submit" value="Upload">
            </form>
        '''

def analyze_image(encoding):
    # Username face encodings
    user_encodings = []
    dir_user_encodings = './user_encodings'

    for username in os.listdir(dir_user_encodings):
        full_path = os.path.join(dir_user_encodings, username)
        user_encoding = pickle.load(open(full_path, "rb"))
        user_encodings.append((username, user_encoding))

    is_registered = False
    user = ''
    action = ''

    # See if the first face in the uploaded image matches the known face of a user
    for (name, u_encoding) in user_encodings:
        match_results = face_recognition.compare_faces([u_encoding], encoding)
        if match_results[0]:
            is_registered = True
            user = name.split('.')[0]
            break

    if is_registered:
        action = 'log in'
    else:
        action = 'register user'

    # Return the result as json
    result = {
        "is_registered": is_registered,
        "user_name": user,
        "action": action,
        "new_img_name": '' if is_registered else 'user_' + str(len(user_encodings))
    }
    return result

@app.route('/profile', methods=['GET'])
@cross_origin()
def profile():
    username = request.headers.get('auth')
    try:
        return send_from_directory('./user_pictures', filename=username + '.png')
    except FileNotFoundError:
        abort(404)

@app.route('/emotion', methods=['POST'])
@cross_origin()
def emotion():
    file = request.files['file']
    if file:
        print(file)
        pil_image = Image.open(file).convert('RGB')
        open_cv_image = np.array(pil_image)

        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        return jsonify(detect_emotion(open_cv_image))

def detect_emotion(face_image):
    label_map = {
        0: 'Angry',
        5: 'Sad',
        4: 'Neutral',
        1: 'Disgust',
        6: 'Surprise',
        2: 'Fear',
        3: 'Happy'
    }

    # get the first face you find, and create a crop out of it
    face_locations = face_recognition.face_locations(face_image)
    top, right, bottom, left = face_locations[0]
    face_image = face_image[top:bottom, left:right]

    # resize, filter and reshape the image to comply to the trained model input schema
    face_image = cv2.resize(face_image, (48, 48))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])

    # load model
    model = load_model("./models/model_v6_23.hdf5")

    # predict class (as int)
    predicted_class = np.argmax(model.predict(face_image))

    # translate prediction into emotion
    predicted_label = label_map[predicted_class]

    return predicted_label

@app.route('/emotion_luxand', methods=['POST'])
@cross_origin()
def emotion_luxand():
  file = request.files['file']
  if file:
    client = luxand("500b2ae817f747f980a68cdb8691b910")

    img = Image.open(file).copy()
    filename = './temp/' + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + '.png'
    img.save(filename, 'PNG')

    return jsonify(client.emotions(photo = filename))

def detect_emotion_luxand():
    client = luxand("500b2ae817f747f980a68cdb8691b910")

    for i in range(1, 10):
        result = client.emotions(photo = "./children/{0}.jpg".format(i))
        print(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    # detect_emotion_luxand()
