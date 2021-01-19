from flask import Flask
from Models.Detectron2.DetectronWrapper import DetectronWrapper
import pypyodbc
from flask_cors import CORS, cross_origin

# context = ('certificate.pem', 'key.pem')

app = Flask(__name__)

cors = CORS(app)
app.config['CORS-HEADERS'] = 'Content-Type'
detectron = DetectronWrapper()


connection = pypyodbc.connect('Driver={SQL Server};Server=DESKTOP-Q69GVDD;Database=MedicalAssistant')

cursor = connection.cursor()

# if __name__ == "__main__":
#     app.run(host='192.168.100.7')

from app import routes
