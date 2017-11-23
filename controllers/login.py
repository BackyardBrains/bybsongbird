from flask import *
from passlib.hash import pbkdf2_sha512 as hasher

login = Blueprint('login', __name__, template_folder='templates')
from extensions import *
from flask_login import *
from _mysql import escape_string


@login.route('/api/login', methods=['POST'])
def login_route():
    logout_user()
    username = request.form['username']
    password = request.form['password']
    with connect_to_database() as cur:
        cur.execute("SELECT password FROM userInfo WHERE username='%s';" % escape_string(username))
        db_response = cur.fetchone()
    if not db_response:
        return json.dumps({'error': 'Incorrect username\n'}), 422
    correct_password = db_response['password']
    login_successful = hasher.verify(password, correct_password)
    if login_successful:
        if request.form['remember'] == u'true':
            remember = True
        else:
            remember = False
        login_user(User(username), remember=remember)
        return json.dumps({}), 200
    else:
        return json.dumps({'error': 'Incorrect password\n'}), 422


@login.route('/api/logout', methods=['POST'])
@login_required
def logout_route():
    logout_user()
    return json.dumps({}), 200


@login.route('/login', methods=['GET'])
def login_page_route():
    options = {}
    active_login = current_user.get_id()
    if active_login:
        return redirect(url_for('main.main_route'))
    return render_template("login.html", **options)


@login.route('/api/current-user', methods=['GET'])
def current_user_route():
    return json.dumps({'current_user': current_user.get_id()})
