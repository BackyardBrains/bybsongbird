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
from machine_learning_and_dsp.process_and_categorize import classiFier
import numpy as np
from extensions import connect_to_database

upload = Blueprint('upload', __name__, template_folder='templates')

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
            

            # model_file = '/vagrant/bybsongbird/model2/model'
            model_file = '/home/ubuntu/bybsongbird/model2/model'
            #model_file = 'C:\\Users\\chouw\\Documents\\bybsongbird\\model2\\model'

            identify = classiFier(model_file=model_file, verbose=True)
            result = identify.classFile(os.path.join(config.env['UPLOAD_FOLDER'], filename))
            first_match = {"name": result['values'][8].split('_')[0].replace("'",""), "percentage": "{:.3%}".format(float(result['values'][9]))}
            second_match = {"name": result['values'][10].split('_')[0].replace("'",""), "percentage": "{:.3%}".format(float(result['values'][11]))}
            third_match = {"name": result['values'][12].split('_')[0].replace("'",""), "percentage": "{:.3%}".format(float(result['values'][13]))}
            
            db = connect_to_database()
            cur = db.cursor()
            add_song = ("UPDATE sampleInfo SET latitude = %s, longitude = %s, humidity = %s, temp = %s, light = %s WHERE sampleid = %s")
            data_song = (latitude, longitude, humidity, temp, light, result['sample_id'])
            cur.execute(add_song, data_song)
            
            options = {
                "filename": filename,
                'sample_id': result['sample_id'],
                'first_match': first_match,
                'second_match': second_match,
                'third_match': third_match
            }

            return render_template("upload.html", **options)

    return render_template("upload.html")
