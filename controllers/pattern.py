from flask import *
import extensions
from flask import url_for

pattern = Blueprint('pattern', __name__, template_folder='templates')

@pattern.route('/pattern', methods = ['GET', 'POST'])
def pattern_route():
	options = {

	}
	return render_template("pattern.html", **options)
