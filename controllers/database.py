from flask import *
from extensions import connect_to_database
from flask import url_for

database = Blueprint('database', __name__, template_folder='templates')

@database.route('/database', methods = ['GET', 'POST'])
def database_route():
	options = {
	
	}
	return render_template("database.html", **options)
