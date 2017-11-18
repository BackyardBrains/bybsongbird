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

        files = request.files.getlist('file')
        
        model_file = '/vagrant/bybsongbird/model2/model'
        # model_file = '/home/ubuntu/bybsongbird/model2/model'
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
                # user_waveform_file = user_file.replace(user_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                user_waveform_file = user_file.replace(user_file.split('.')[-1], 'png').replace('/home/ubuntu/bybsongbird', '')
            
                result = identify.classFile(user_file)
                first_match = [{"name": result["values"][8].split("_")[0].replace("'",""), "value": float(result["values"][9])}, {"name": "other", "value": 1 - float(result["values"][9])}]
                second_match = [{"name": result["values"][10].split("_")[0].replace("'",""), "value": float(result["values"][11])}, {"name": "other", "value": 1 - float(result["values"][11])}]
                third_match = [{"name": result["values"][12].split("_")[0].replace("'",""), "value": float(result["values"][13])}, {"name": "other", "value": 1 - float(result["values"][13])}]

                activity_file = os.path.join(config.env['UPLOAD_FOLDER'], 'activity/' + filename)
                activity_waveform = Waveform(activity_file)
                activity_waveform.save()
                activity_waveform_file = activity_file.replace(activity_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                # activity_file = activity_file.replace('/vagrant/bybsongbird', '..')
                activity_file = activity_file.replace('/home/ubuntu/bybsongbird', '..')

                noise_file = os.path.join(config.env['UPLOAD_FOLDER'], 'noise/' + filename)
                noise_waveform = Waveform(noise_file)
                noise_waveform.save()
                noise_waveform_file = noise_file.replace(noise_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                # noise_file = noise_file.replace('/vagrant/bybsongbird', '..')
                noise_file = noise_file.replace('/home/ubuntu/bybsongbird', '..')

                user_clean_file = os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + filename)
                user_clean_waveform = Waveform(user_clean_file)
                user_clean_waveform.save()
                user_clean_waveform_file = user_clean_file.replace(user_clean_file.split('.')[-1], 'png').replace('/vagrant/bybsongbird', '')
                # user_clean_file = user_clean_file.replace('/vagrant/bybsongbird', '..')
                user_clean_file = user_clean_file.replace('/home/ubuntu/bybsongbird', '..')

                cur = db.cursor()
                cur.execute("SELECT * FROM sampleInfo WHERE sampleid = %s", (result['sample_id'], ))
                result_sample = cur.fetchall()
                latitude = result_sample[0]['latitude']
                longitude = result_sample[0]['longitude']
                humidity = result_sample[0]['humidity']
                temp = result_sample[0]['temp']
                light = result_sample[0]['light']

                matches.append({
                                'user': user_waveform_file,
                                'filename': filename, 
                                'sample_id': result['sample_id'], 
                                'first_match': json.dumps(first_match),
                                'second_match': json.dumps(second_match),
                                'third_match': json.dumps(third_match),
                                'activity': activity_waveform_file,
                                'activity_audio': activity_file,
                                'noise': noise_waveform_file,
                                'noise_audio': noise_file,
                                'user_clean': user_clean_waveform_file,
                                'user_clean_audio': user_clean_file,
                                'file_num': file_num,
                                'latitude': latitude,
                                'longitude': longitude,
                                'humidity': humidity,
                                'temperature': temp,
                                'light': light
                                })
        
        options = {
            'matches': matches,
        }
        
        return render_template("upload.html", **options)

    return render_template("upload.html")