import os
import pathlib
import zipfile

import flask
import pydicom
import pydicom._storage_sopclass_uids
from dicom.dataset import Dataset
from flask import request, abort, send_from_directory
from flask_cors import CORS
from pydicom.dataset import Dataset
from pydicom.uid import ExplicitVRLittleEndian
from datetime import datetime

import UNet.main as UNet
import csv

UPLOAD_FOLDER_HEAD = 'images'
UPLOAD_FOLDER = os.path.join('images', 'User')
UPLOAD_FOLDER_ANALYZED = os.path.join('images', 'User', 'Analyzed')

app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True


def is_null_or_empty_string(variable):
    return variable == None or variable == '' or variable.isspace()


def user_exists(username):
    csv_reader = open('users.csv', 'r')
    with csv_reader:
        for row in csv_reader:
            stored_username = row[0]

            if username == stored_username:
                return True
    return False


@app.route('/auth', methods=['POST'])
def signin():
    username = request.get_json()['username']
    password = request.get_json()['password']

    if is_null_or_empty_string(username) and is_null_or_empty_string(password):
        abort(400, "Username and password must have at least one character.")

    correct_credentials = False
    csv_reader = open('users.csv', 'r')
    with csv_reader:
        for row in csv_reader:
            if is_null_or_empty_string(row):
                continue

            stored_username = row.split(",")[0].strip()
            stored_password = row.split(",")[1].strip()

            if username == stored_username and password == stored_password:
                correct_credentials = True
                break

    if not correct_credentials:
        raise abort(401, "Username or password is wrong.")

    return username


@app.route('/user', methods=['POST'])
def signup():
    username = request.get_json()['username'].strip()
    password = request.get_json()['password'].strip()

    if is_null_or_empty_string(username) and is_null_or_empty_string(password):
        abort(400, "Username and password must have at least one character.")

    if user_exists(username):
        abort(409, "Username is taken.")

    line = [username, password]
    csv_writer = open('users.csv', 'a')
    with csv_writer:
        writer = csv.writer(csv_writer)
        writer.writerow(line)

    return 'created'


# HTTP Request Handlers
@app.route('/images', methods=['POST'])
def images_post():
    username = request.headers.get("username")

    if username:
        return upload_logged_user(username)
    return upload()


@app.route('/analyzed_images/<filename>', methods=['GET'])
def images_get(filename):
    username = request.args.get("username")
    return download(filename, username)


@app.route('/my_images', methods=['GET'])
def get_user_images():
    username = request.headers.get("username")
    if not username:
        abort(401)

    folder_names = get_user_folder_names(username)
    response = {
        "folders": folder_names,
    }
    return response


# GET
def download(filename, username=None):
    if username:
        user_folder_analyzed = get_user_folder_analyzed(os.path.join(get_user_folder(username), filename), True)
        folder_path_absolute = os.path.join(pathlib.Path().absolute(), user_folder_analyzed)
        filename = "Files.zip"
    else:
        folder_path_absolute = os.path.join(pathlib.Path().absolute(), UPLOAD_FOLDER_ANALYZED)
    return send_from_directory(directory=folder_path_absolute, filename=filename)


def get_user_folder_names(username):
    folder_names = []

    user_folder = get_user_folder(username)
    for filename in os.listdir(user_folder):
        folder_path = os.path.join(user_folder, filename)
        if os.path.isdir(folder_path):
            head, folder_name = os.path.split(folder_path)
            folder_names.append(folder_name)

    return folder_names


def get_user_folder(username):
    return get_relative_path(username, UPLOAD_FOLDER_HEAD)


# POST
def upload():
    received_files = request.files.items()

    clean_upload_folders()
    save_files(received_files)
    predictions = analyze_images()
    analyzed_file_names = save_images(predictions)

    zip_name = create_zip(analyzed_file_names)
    response = {
        "filename": zip_name
    }
    return response


def upload_logged_user(username):
    received_files = request.files.items()

    now = datetime.now()
    user_now_folder = get_user_now_folder(now, username)
    save_files(received_files, user_now_folder)

    predictions = analyze_images(get_user_now_folder_head(user_now_folder))
    user_now_folder_analyzed = get_user_folder_analyzed(user_now_folder)
    analyzed_file_names = save_images(predictions, user_now_folder_analyzed)

    zip_name = create_zip(analyzed_file_names, user_now_folder_analyzed)
    response = {
        "filename": zip_name
    }
    return response


def get_user_now_folder(now, username):
    user_now_folder = get_relative_path(os.path.join(username, now.strftime("%Y%m%d_%H%M%S")), UPLOAD_FOLDER_HEAD)
    return os.path.join(user_now_folder, "upload")


def get_user_now_folder_head(user_now_folder):
    head, tail = os.path.split(user_now_folder)
    return head


def get_user_folder_analyzed(user_now_folder, add_upload=False):
    if add_upload:
        return os.path.join(user_now_folder, "upload", "Analyzed")
    return os.path.join(user_now_folder, "Analyzed")


# Analyze images
def analyze_images(head_folder_path=UPLOAD_FOLDER_HEAD):
    absolute_folder_path = os.path.join(pathlib.Path().absolute(), head_folder_path)
    return UNet.predict(absolute_folder_path)


# Save files
def save_files(files, relative_folder_path=UPLOAD_FOLDER):
    saved_file_names = []
    for fileName, file in files:
        if file is None or file.filename == '':
            abort(400)
        save_file(file, relative_folder_path)
        saved_file_names.append(fileName)
    return saved_file_names


def save_file(file, relative_folder_path):
    create_directory_if_not_exists(relative_folder_path, True)
    file.save(get_absolute_path(file.filename, relative_folder_path))


def create_directory_if_not_exists(relative_path, is_directory_path):
    if is_directory_path:
        relative_path = os.path.join(relative_path, 'some_file')
    if not os.path.exists(os.path.dirname(relative_path)):
        os.makedirs(os.path.dirname(relative_path))


def create_zip(file_names, path_to_folder=UPLOAD_FOLDER_ANALYZED):
    zip_name = 'Files.zip'
    zip_path = get_relative_path(zip_name, path_to_folder)
    zipFolder = zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED)

    for fileName in file_names:
        filePath = get_relative_path(fileName, path_to_folder)
        zipFolder.write(filePath, fileName)

    zipFolder.close()
    return zip_name


def clean_upload_folders():
    clean_folder(UPLOAD_FOLDER)
    clean_folder(UPLOAD_FOLDER_ANALYZED)


def clean_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def save_images(predictions, user_now_folder=UPLOAD_FOLDER_ANALYZED):
    file_names = []
    index = 1
    for numpy_image in predictions:
        file_name = "image_" + str(index) + ".dcm"
        path_to_file = get_absolute_path(file_name, user_now_folder)

        write_dicom(numpy_image, path_to_file)
        file_names.append(file_name)
        index = index + 1

    return file_names


def write_dicom(pixel_array, path_to_file):
    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    ds = Dataset()
    ds.file_meta = meta
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    ds.PatientName = "PatientName"
    ds.PatientID = "123456"
    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15
    ds.ImagesInAcquisition = "1"
    ds.Rows = pixel_array.shape[0]
    ds.Columns = pixel_array.shape[1]
    ds.InstanceNumber = 1
    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1
    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)

    ds.PixelData = pixel_array.tobytes()
    create_directory_if_not_exists(path_to_file, False)
    ds.save_as(path_to_file, True)


# Read files
def read_files(file_names):
    files = []
    for fileName in file_names:
        file = read_file(fileName)
        files.append(file)
    return files


def read_file(fileName):
    return open(get_relative_path(fileName), mode='rb').read()


def get_relative_path(fileName, relative_folder_path=UPLOAD_FOLDER):
    return os.path.join(relative_folder_path, fileName)


def get_absolute_path(fileName, relative_folder_path=UPLOAD_FOLDER):
    """
    Creates and returns an absolute path for the file, considering that the file is stored in the provided folder.
    """
    absolute_folder_path = os.path.join(pathlib.Path().absolute(), relative_folder_path)
    return os.path.join(absolute_folder_path, fileName)


def run():
    app.run()
