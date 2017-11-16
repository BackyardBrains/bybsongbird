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
import json
from waveform import Waveform

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

        # file = request.files['file']
        files = request.files.getlist('file')
        
        model_file = '/vagrant/bybsongbird/model2/model'
        # model_file = '/w/bybsongbird/model2/model'
        identify = classiFier(model_file=model_file, verbose=True)

        matches = []
        
        file_num = len(files)
        for file in files:
            if file.filename == '':
                options = {
                    "emptyname": True
                }
                return render_template("upload.html", **options)

            else:
                filename = secure_filename(file.filename)
                user_file = os.path.join(config.env['UPLOAD_FOLDER'], filename)
                file.save(user_file)            
                user_waveform = Waveform(user_file)
                user_waveform.save()
                user_waveform_file = user_file.replace(user_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
            
                # result = identify.classFile(user_file)
                # match = []
                # first_match = {"name": result["values"][8].split("_")[0].replace("'",""), "value": float(result["values"][9]), "percentage": "{:.3%}".format(float(result["values"][9]))}
                # second_match = {"name": result["values"][10].split("_")[0].replace("'",""), "value": float(result["values"][11]), "percentage": "{:.3%}".format(float(result["values"][11]))}
                # third_match = {"name": result["values"][12].split("_")[0].replace("'",""), "value": float(result["values"][13]), "percentage": "{:.3%}".format(float(result["values"][13]))}
                # value_other = 1 - float(result["values"][9]) - float(result["values"][11]) - float(result["values"][13])
                # ohter_match = {"name": "other birds", "value": value_other, "percentage": "{:.3%}".format(value_other)}
                # match.append(first_match)
                # match.append(second_match)
                # match.append(third_match)
                # match.append(ohter_match)
                # match.sort(key=lambda x: x['value'], reverse=True)

                activity_file = os.path.join(config.env['UPLOAD_FOLDER'], 'activity/' + filename)
                activity_waveform = Waveform(activity_file)
                activity_waveform.save()
                activity_waveform_file = activity_file.replace(activity_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                activity_file = activity_file.replace('/vagrant/bybsongbird', '..')

                noise_file = os.path.join(config.env['UPLOAD_FOLDER'], 'noise/' + filename)
                noise_waveform = Waveform(noise_file)
                noise_waveform.save()
                noise_waveform_file = noise_file.replace(noise_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                noise_file = noise_file.replace('/vagrant/bybsongbird', '..')

                user_clean_file = os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + filename)
                user_clean_waveform = Waveform(user_clean_file)
                user_clean_waveform.save()
                user_clean_waveform_file = user_clean_file.replace(user_clean_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                user_clean_file = user_clean_file.replace('/vagrant/bybsongbird', '..')

                matches.append({'user': user_waveform_file,
                                'filename': filename, 
                                # 'sample_id': result['sample_id'], 
                                # 'match': json.dumps(match),
                                'activity': activity_waveform_file,
                                'activity_audio': activity_file,
                                'noise': noise_waveform_file,
                                'noise_audio': noise_file,
                                'user_clean': user_clean_waveform_file,
                                'user_clean_audio': user_clean_file,
                                'file_num': file_num
                                })

                # cur = db.cursor()
                # add_song = ("UPDATE sampleInfo SET latitude = %s, longitude = %s, humidity = %s, temp = %s, light = %s WHERE sampleid = %s")
                # data_song = (latitude, longitude, humidity, temp, light, result['sample_id'])
                # cur.execute(add_song, data_song)

        
        options = {
            'matches': matches,
        }
        
        return render_template("upload.html", **options)

    return render_template("upload.html")