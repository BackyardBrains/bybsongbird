from flask import *
from flask import url_for
from flask import send_file
import extensions
import sys

sys.path.append('/home/bybsongbird/app/bybsongbird/static/songs/users')

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api', methods = ['GET', 'POST'])
def api_route():

    #open db connection and open cursor and execute. See MySQL documentation for cursors with Python
    db = extensions.connect_to_database()
    cur = db.cursor()
    result = ''
    cur.execute("SELECT * FROM sampleInfo")
    samples = cur.fetchone() 
     
    #convert data into strings 
    sampleList = [] 
    while samples is not None:
	  sampleList.append(str(samples))
          samples = cur.fetchone()
    
    
    
    string = "$$$ BEGIN NEXT DATA $$$"	
    return string.join(sampleList)



    #return send_file('/home/bybsongbird/app/bybsongbird/static/songs/users/-1713581483.WAV', attachment_filename='-1713581483.WAV') 
