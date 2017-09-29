from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import os
import hashlib
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import datetime
from process_and_categorize import classiFier
import numpy as np

upload = Blueprint('upload', __name__, template_folder='templates')

db = extensions.connect_to_database()

ALLOWED_EXTENSIONS = set(['pcm', 'wav', 'aiff', 'mp3', 'aac', 'ogg', 'wma', 'flac', 'alac', 'wma'])

@upload.route('/upload', methods = ['GET','POST'])
def upload_route():
    if request.method == 'POST':
        if 'file' not in request.files:
            options = {
                "noFile": True
            }
            return render_template("upload.html", **options)

        file = request.files['file']

        if file.filename == '':
            options = {
                "emptyname": True
            }
            return render_template("upload.html", **options)

        else:
            latitude_get = request.form['latitude']
            if latitude_get != '':
                latitude = float(latitude_get)
            else:
                latitude = None

            longitude_get = request.form['longitude']
            if longitude_get != '':
                longitude = float(longitude_get)
            else:
                longitude = None

            humidity_get = request.form['humidity']
            if humidity_get != '':
                humidity = float(humidity_get)
            else:
                humidity = None

            temp_get = request.form['temp']
            if temp_get != '':
                temp = float(temp_get)
            else:
                temp = None

            light_get = request.form['light']
            if light_get != '':
                light = float(light_get)
            else:
                light = None

            filename = secure_filename(file.filename)
            file.save(os.path.join(config.env['UPLOAD_FOLDER'], filename))
            

            model_file = '/vagrant/bybsongbird/model2/model'
            # model_file = '/w/bybsongbird/model2/model'

            identify = classiFier(model_file=model_file, verbose=True)
            result = identify.classFile(os.path.join(config.env['UPLOAD_FOLDER'], filename))
            sorted_index = np.argsort(result['P'])
            first_match = {"name": result['classNames'][sorted_index[-1]].split('_')[0], "percentage": "{:.2%}".format(result['P'][sorted_index[-1]])}
            second_match = {"name": result['classNames'][sorted_index[-2]].split('_')[0], "percentage": "{:.2%}".format(result['P'][sorted_index[-2]])}
            third_match = {"name": result['classNames'][sorted_index[-3]].split('_')[0], "percentage": "{:.2%}".format(result['P'][sorted_index[-3]])}
            
            cur = db.cursor()
            add_song = ("INSERT INTO sampleInfo (deviceid, added, latitude, longitude, humidity, temp, light, type1, per1, type2, per2, type3, per3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_song = (-1, datetime.datetime.now(), latitude, longitude, humidity, temp, light, "bird1", 0.85, "bird2", 0.35, "bird3", 0.05)
            cur.execute(add_song, data_song)
            
            options = {
                "filename": filename,
                'first_match': first_match,
                'second_match': second_match,
                'third_match': third_match
            }

            return render_template("upload.html", **options)

    return render_template("upload.html")