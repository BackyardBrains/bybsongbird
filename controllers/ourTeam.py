from flask import *

ourTeam = Blueprint('ourTeam', __name__, template_folder='templates')


@ourTeam.route('/ourTeam', methods=['GET'])
def ourTeam_route():
    options = {
    }
    return render_template("ourTeam.html", **options)
