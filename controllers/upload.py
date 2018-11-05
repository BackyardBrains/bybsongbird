
import json
import os
from zlib import crc32

from flask import *
from flask import request
from flask_login import login_required, current_user
from werkzeug import secure_filename
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

import config
import extensions
from bybsongbird.machine_learning_and_dsp.process_and_categorize import classiFier
from bybsongbird.waveform import Waveform

upload = Blueprint('upload', __name__, template_folder='templates')

#db = extensions.connect_to_database()

ALLOWED_EXTENSIONS = set(['pcm', 'wav', 'aiff', 'mp3', 'aac', 'ogg', 'wma', 'flac', 'alac', 'wma'])

@upload.route('/upload', methods = ['GET','POST'])
@login_required
def upload_route():
    if request.method == 'POST': #Post request means a file is requested to be uploaded
        if 'file' not in request.files:
            options = {
                "noFile": True
            }
            return render_template("upload.html", **options)

        files = request.files.getlist('file') #gets a list of files posted to the url
        model_file = os.path.join(os.getcwd(), 'model2', 'model') #gets model file
        identify = classiFier(model_file=model_file, verbose=True) #creates a Classifier object (see process and catagorize under machine_learning_and_dsp)

        matches = []
        file_num = len(files)
        for file in files: #iterate through posted files and classify them
            if file.filename == '':
                options = {
                    "emptyname": True
                }
                return render_template("upload.html", **options)

            else:
                filename = secure_filename(file.filename)
                user_file_temp = os.path.join(config.env['UPLOAD_FOLDER'], filename)
                
		file.save(user_file_temp) #if filename is not empty, save the file under a temp name

                with open(user_file_temp, 'rb') as file_contents:
                    sample_id = crc32(file_contents.read()) #create a checksum from file contents to use as id

                filename = str(sample_id) + file.filename[len(file.filename)-4: len(file.filename)] #create filename from id
                user_file = os.path.join(config.env['UPLOAD_FOLDER'], filename) #get upload folder
                os.rename(user_file_temp, user_file) #re-write temp file name with id based filename
		
		if file.filename[len(file.filename)-3:len(file.filename)].lower() == 'mp3': #if the file is an mp3, re-write as a WAV
		    AudioSegment.from_mp3(user_file).export(user_file[0:len(user_file)-3] + "wav", format="wav")
		    filename = filename[0:len(filename)-3] + 'wav'
		    user_file = user_file[0:len(user_file)-3] + 'wav'

                result = identify.classFile(user_file, username=current_user.get_id()) #classify the file using the loaded model
                #get first, second, and third top matches
                first_match_name = result["values"][8]
                first_match = [{"name": first_match_name[1:first_match_name.find('_')].title(), "value": float(result["values"][9])}, {"name": "Other", "value": 1 - float(result["values"][9])}]
                second_match_name = result["values"][10]
                second_match = [{"name": second_match_name[1:second_match_name.find('_')].title(), "value": float(result["values"][11])}, {"name": "Other", "value": 1 - float(result["values"][11])}]
                third_match_name = result["values"][12]
                third_match = [{"name": third_match_name[1:third_match_name.find('_')].title(), "value": float(result["values"][13])}, {"name": "Other", "value": 1 - float(result["values"][13])}]

                user_waveform = Waveform(user_file) #Create a waveform object from the saved file (see Waveform.py)
                user_waveform.save()
                user_waveform_file = user_file.replace(user_file.split('.')[-1], 'png').replace(os.getcwd(), '') #save the waveform file
                user_file = user_file.replace(os.getcwd(), '..')

                activity_file = os.path.join(config.env['UPLOAD_FOLDER'], 'activity/' + filename) #file with song activity
                if os.path.isfile(activity_file):
                    activity_waveform = Waveform(activity_file)
                    activity_waveform.save()
                    activity_waveform_file = activity_file.replace(activity_file.split('.')[-1], 'png').replace(os.getcwd(), '')
                    activity_file = activity_file.replace(os.getcwd(), '..')
                else:
                    activity_waveform_file = None
                    activity_file = None

                noise_file = os.path.join(config.env['UPLOAD_FOLDER'], 'noise/' + filename) #file with noise still in it
                if os.path.isfile(noise_file):
                    noise_waveform = Waveform(noise_file)
                    noise_waveform.save()
                    noise_waveform_file = noise_file.replace(noise_file.split('.')[-1], 'png').replace(os.getcwd(), '')
                    noise_file = noise_file.replace(os.getcwd(), '..')
                else:
                    noise_waveform_file = None
                    noise_file = None

                user_clean_file = os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + filename) #cleaned file
                if os.path.isfile(user_clean_file):
                    user_clean_waveform = Waveform(user_clean_file)
                    user_clean_waveform.save()
                    user_clean_waveform_file = user_clean_file.replace(user_clean_file.split('.')[-1], 'png').replace(os.getcwd(), '')
                    user_clean_file = user_clean_file.replace(os.getcwd(), '..')
                else:
                    user_clean_waveform_file = None
                    user_clean_file = None
		

        	db = extensions.connect_to_database()  #open a database curson to MySQLdb
 
                cur = db.cursor()
                cur.execute("SELECT * FROM sampleInfo WHERE sampleid = %s", (result['sample_id'], ))
                result_sample = cur.fetchall() #get results from the executed SQL cmd above
		
		cur.close() 

                #Get sample metadata
                latitude = result_sample[0]['latitude']
                longitude = result_sample[0]['longitude']
                humidity = result_sample[0]['humidity']
                temp = result_sample[0]['temp']
                if temp:
                    temp = int(round(temp))
                light = result_sample[0]['light']
                if light:
                    light = int(round(light))

                #add file info to the matches array, which starts [] at the top of this file
                matches.append({
                                'user': user_waveform_file,
                                'filename': user_file,
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
      
        return render_template("upload.html", **options) #returns .html template

    return render_template("upload.html")
