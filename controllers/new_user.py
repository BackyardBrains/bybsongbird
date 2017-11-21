from flask import *

new_user = Blueprint('new_user', __name__, template_folder='templates')
from extensions import *
from passlib.hash import pbkdf2_sha512 as hasher


@new_user.route('/api/new_user', methods=['POST'])
def upload_route():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if len(username) > 256:
        return json.dumps({'error': 'Username cannot be more than 256 characters long.\n'}), 409
    if len(password) > 256:
        return json.dumps({'error': 'Password cannot be more than 256 characters long.\n'}), 409
    if password != confirm_password:
        return json.dumps({'error': 'Passwords do not match.\n'}), 409
    with connect_to_database() as cur:
        cur.execute("SELECT EXISTS(SELECT 1 FROM userInfo WHERE username = '%s');" % username)
        cur_response = cur.fetchone()
        user_exists = cur_response.items()[0][1]
        if user_exists:
            user_conflict_json = json.dumps({'error': 'Username is already taken.\n'})
            return user_conflict_json, 409

        hashed_password = hasher.hash(password)
        cur.execute("INSERT INTO userInfo (username, password) values ('%s', '%s');" % (username, hashed_password))
        return json.dumps({}), 200
