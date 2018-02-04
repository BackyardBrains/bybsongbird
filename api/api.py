from flask import *
from flask import url_for
from flask import send_file
import extensions
import sys

sys.path.append('/home/bybsongbird/app/bybsongbird/static/songs/users')

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api', methods = ['GET', 'POST'])
def api_route():
    db = extensions.connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM sampleInfo")
    result = cur.fetchall()
    temp = result[0]['temp'] 
    temp = str(temp)
    
    return send_file('/home/bybsongbird/app/bybsongbird/static/songs/users/-1713581483.WAV', attachment_filename='-1713581483.WAV') 
