from flask import Flask, redirect, url_for, Blueprint
from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import hash

logout = Blueprint('logout', __name__, template_folder='templates')

@logout.route('/logout')
def logout_route():
        session.pop('username', None)
        return redirect(url_for('main.main_route'))