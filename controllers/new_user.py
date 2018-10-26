from flask import *

new_user = Blueprint('new_user', __name__, template_folder='templates')
from bybsongbird.extensions import *
from passlib.hash import pbkdf2_sha512
from _mysql import escape_string


@new_user.route('/api/new_user', methods=['POST'])
def new_user_route():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if len(username) > 256:
        return json.dumps({'error': 'Username cannot be more than 256 characters long\n'}), 409
    if len(password) > 256:
        return json.dumps({'error': 'Password cannot be more than 256 characters long\n'}), 409
    if not len(username):
        return json.dumps({'error': 'Username cannot be left blank\n'}), 409
    if not len(password):
        return json.dumps({'error': 'Password cannot be left blank\n'}), 409
    if password != confirm_password:
        return json.dumps({'error': 'Passwords do not match\n'}), 409
    with connect_to_database() as cur:
        cur.execute("SELECT EXISTS(SELECT 1 FROM userInfo WHERE username = '%s');" % escape_string(username))
        cur_response = cur.fetchone()
        user_exists = cur_response.items()[0][1]
        if user_exists:
            user_conflict_json = json.dumps({'error': 'Username is already taken\n'})
            return user_conflict_json, 409

        hash_handler = pbkdf2_sha512.using(rounds=123456)
        hashed_password = hash_handler.hash(password)
        cur.execute("INSERT INTO userInfo (username, password) values ('%s', '%s');" % (
        escape_string(username), hashed_password))
        return json.dumps({}), 200


@new_user.route('/new-user', methods=['GET'])
def new_user_page_route():
    options = {}
    return render_template("new_user.html", **options)
