from flask import *
from flask import url_for
from flask import send_file
from flask import jsonify

import sys
sys.path.append('/home/bybsongbird/app/bybsongbird')
import config

import os
import json
from zlib import crc32
from flask import request

sys.path.append('/home/bybsongbird/app/bybsongbird/static/songs/users')

@uploadTest = Blueprint('/uploadTest', __name__, template_folder='templates')

@uploadTest.route('/uploadTest', methods = ['POST'])
def uploadTest_route():
	return jsonify({'name': name, 'data': data})
