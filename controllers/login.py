from flask import *
from passlib.hash import pbkdf2_sha512 as hasher

login = Blueprint('login', __name__, template_folder='templates')
from extensions import *
from flask_login import *


@login.route('/api/login', methods=['POST'])
def login_route():
    logout_user()
    username = request.form['username']
    password = request.form['password']
    with connect_to_database() as cur:
        cur.execute("SELECT password FROM userInfo WHERE username='%s';" % username)
        db_response = cur.fetchone()
    if not db_response:
        return json.dumps({'error': 'Incorrect username.\n'}), 422
    correct_password = db_response['password']
    login_successful = hasher.verify(password, correct_password)
    if login_successful:
        if request.form['remember'] == u'True':
            remember = True
        else:
            remember = False
        login_user(User(username), remember=remember)
        return json.dumps({}), 200
    else:
        return json.dumps({'error': 'Incorrect password.\n'}), 422


@login.route('/api/logout', methods=['POST'])
@login_required
def logout_route():
    logout_user()
    return json.dumps({}), 200
