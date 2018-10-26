from flask import *
from passlib.hash import pbkdf2_sha512 as hasher

login = Blueprint('login', __name__, template_folder='templates')
from bybsongbird.extensions import *
from flask_login import login_required, login_user, current_user, logout_user
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


@login.route('/api/change-password', methods=['POST'])
@login_required
def change_password_route():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_new_password = request.form['confirm_new_password']
    if len(new_password) > 256:
        return json.dumps({'error': 'New password cannot be more than 256 characters long\n'}), 409
    if new_password != confirm_new_password:
        return json.dumps({'error': 'New passwords do not match\n'}), 409

    username = current_user.get_id()
    with connect_to_database() as cur:
        cur.execute("SELECT password FROM userInfo WHERE username='%s';" % username)
        db_response = cur.fetchone()

    correct_password = db_response['password']
    correct_old_password = hasher.verify(old_password, correct_password)

    if correct_old_password:
        hashed_new_password = hasher.hash(new_password)
        with connect_to_database() as cur:
            cur.execute("UPDATE userInfo SET password='%s' WHERE username='%s';" % (hashed_new_password, username))
        return json.dumps({'success': 'Password changed successfully\n'}), 200
    else:
        return json.dumps({'error': 'Old password is incorrect\n'}), 409


@login.route('/settings', methods=['GET'])
@login_required
def settings_route():
    return render_template('settings.html')
