from app import app, cross_origin, detectron, cursor, connection
from flask import request, render_template
import json
import uuid
import os
from Domain.HistoryRecords import HistoryRecords
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    # cursor.execute("select * from Users")
    #
    # result = "Users:\n\n"
    #
    # for row in cursor:
    #     for x in row:
    #         result += str(x)
    #         result += '\n\n'
    #
    # return result
    return "Hello world"
    # return render_template('templates/index.html')  # Return index.html


@app.route('/login_server', methods=['POST'])
def login_server():
    email = request.json["Email"]
    password = request.json["Password"]

    cursor.execute("select UserID from users where Email='" + email + "' and Password='" + password + "'")

    result = cursor.fetchone()

    code = 200
    error = ""
    userID = ""

    if result is None:
        code = 404
        error = "Login failed. User does not exist!"
    else:
        userID = result[0][2:-1]

    return json.dumps({"userID": str(userID), "code": code, "error": error})


@app.route('/get_user_history_server', methods=['POST'])
def get_user_history_server():
    userID = request.json["userID"]

    print(userID)

    cursor.execute("select * from HistoryRecords where userID='" + userID + "'")

    print("select * from HistoryRecords where userID='" + userID + "'")

    code = 200
    error = ""

    result = []
    for row in cursor:
        hr = HistoryRecords(row[0][2:-1], row[1][2:-1], row[2], row[3])
        result.append(hr.serialize())

    return json.dumps({"userID": str(userID), "code": code, "error": error, "history": result})


@app.route('/register_server', methods=['POST'])
def register_server():
    email = request.json["Email"]
    password = request.json["Password"]

    cursor.execute("select * from users where Email='" + email + "'")

    result = cursor.fetchone()

    code = 200
    error = ""
    userID = ""

    if result is not None:
        code = 404
        error = "Register failed. User already exists!"
    else:
        userID = uuid.uuid1()
        cursor.execute("insert into Users values ('" + str(userID) +
                       "', '" + email + "', '" + password + "')")
        connection.commit()

    return json.dumps({"userID": str(userID), "code": code, "error": error})


@app.route('/analyse_image_server', methods=['POST'])
def analyse_image_server():
    userID = request.json["userID"]
    imageBytes = request.json["imageBytes"]
    imageName = request.json["imageName"]

    code = 200
    error = ""

    imageDate = datetime.now().strftime("%Y-%m-%d %H-%M")

    if userID != "guest":
        recordID = uuid.uuid1()

        cursor.execute("insert into HistoryRecords values ('" + str(recordID) +
                       "', '" + userID + "', '" + imageName + "', '" + imageDate + "')")
        connection.commit()

    resultBytes = detectron.detect_file(userID, imageDate, imageName, imageBytes)

    print(len(resultBytes))

    return json.dumps({"code": code, "error": error, "resultBytes": resultBytes})


# @app.route('/get_images', methods=['POST'])
# @cross_origin()
# def get_images():
#     code = 200
#     error = ""
#
#     resultBytes = get_images_func()
#
#     return json.dumps({"code": code, "error": error, "resultBytes": resultBytes})


@app.route('/get_record_images_server', methods=['POST'])
@cross_origin()
def get_record_images_server():
    recordID = request.json["recordID"]

    cursor.execute("select * from HistoryRecords where RecordID='" + recordID + "'")

    result = cursor.fetchone()

    code = 200
    error = ""
    resultBytes = []

    if result is None:
        code = 404
        error = "Record not found"
    else:
        hr = HistoryRecords(result[0][2:-1], result[1][2:-1], result[2], result[3])
        resultBytes = detectron.get_record_images(hr.userID, hr.imageDate)

    return json.dumps({"code": code, "error": error, "resultBytes": resultBytes})
