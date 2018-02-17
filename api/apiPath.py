
from flask import *
from flask import url_for
from flask import send_file
from flask import jsonify
import extensions
import sys



#This file is for accessing individual file information for the app. URL: ../apiPath/<fileID>/<'info' or 'file'>   'info' option gives info to the file, 'file' gives the audio file itself





sys.path.append('/home/bybsongbird/app/bybsongbird/static/songs/users')

apiPath = Blueprint('apiPath', __name__, template_folder='templates')


@apiPath.route('/apiPath/<postID>/<option>', methods = ['GET'])
def apiPath_route(postID, option): 
    
    #if second URL variable option == "file", return the sound file
    if option == "file":
    	path = '/home/bybsongbird/app/bybsongbird/static/songs/users/' + postID + '.WAV'
    	attachment = postID + '.WAV'	
    	return send_file(path, attachment_filename=attachment)

    #if option == "info", return file 
    if option == "info":
	db = extensions.connect_to_database()
  	cur = db.cursor()
        cur.execute("SELECT * FROM sampleInfo WHERE sampleid = %s", (postID, ))
        result = cur.fetchone()
  	match = {}
	match['sample_id'] = result['sampleid']
	match['first_match'] = json.dumps([{"name": result['type1'][0:result['type1'].find('_')].title(), "value": float(result["per1"])}, {"name": "Other", "value": 1 - float(result["per1"])}])
	match['second_match'] = json.dumps([{"name": result['type2'][0:result['type2'].find('_')].title(), "value": float(result["per2"])}, {"name": "Other", "value": 1 - float(result["per2"])}])
	match['third_match'] = json.dumps([{"name": result['type3'][0:result['type3'].find('_')].title(), "value": float(result["per3"])}, {"name": "Other", "value": 1 - float(result["per3"])}])
	match['added'] = result['added'].strftime("%b %d %Y %X")
	match['latitude'] = result['latitude']
	match['longitude'] = result['longitude']
	match['humidity'] = int(round(result['humidity']))
	match['temperature'] = int(round(result['temp']))
	match['light'] = int(round(result['light']))

	options = {
		"match": match
	}
	return jsonify(options)
