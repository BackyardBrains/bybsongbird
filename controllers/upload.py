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

upload = Blueprint('upload', __name__, template_folder='templates')

db = extensions.connect_to_database()

ALLOWED_EXTENSIONS = set(['pcm', 'wav', 'aiff', 'mp3', 'aac', 'ogg', 'wma', 'flac', 'alac', 'wma'])

@upload.route('/upload', methods = ['GET','POST'])
def upload_route():

	options = {
        
	}
	return render_template("upload.html", **options)