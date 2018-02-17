from flask import *
from flask import url_for
from flask import send_file

import config

import extensions
import sys
import os

sys.path.append('/home/bybsongbird/app/bybsongbird/static/songs/users')

api = Blueprint('api', __name__, template_folder='templates')





#This file is the main page for the app api. Sends entire databse data to app. For sending file to app, see apiPath.py



@api.route('/api', methods = ['GET', 'POST'])
def api_route():

    #open db connection and open cursor and execute. See MySQL documentation for cursors with Python
    db = extensions.connect_to_database()
    cur = db.cursor()
    result = ''
    cur.execute("SELECT * FROM sampleInfo")
    samples = cur.fetchall() 
   
    sampleList = []
    
    for row in samples:
	birdType = row['type1'][0:row['type1'].find('_')]
    	sample = ({
            "per": round(row['per1'] * 100, 2), 
            "type": birdType.title(),
            "date": row['added'].strftime("%b %d %Y"),
            "id": str(row['sampleid']),
	    "lat": str(row['latitude']), 
	    "long": str(row['longitude']), 
	    "temp": str(row['temp']), 
            })
   	sampleList.append(sample) 
     
    options = { 
	"sampleList": sampleList
        }
     
  
    return jsonify(options)


    
     
