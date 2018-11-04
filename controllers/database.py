from flask import *
import extensions
from flask import url_for

database = Blueprint('database', __name__, template_folder='templates')

@database.route('/database', methods = ['GET', 'POST'])
def database_route():
	options = {
	
	}
	return render_template("database.html", **options)
