from flask import *

new_user = Blueprint('new_user', __name__, template_folder='templates')
from extensions import *
import bcrypt
from config import *


@new_user.route('/api/new_user', methods=['POST'])
def upload_route():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    with connect_to_database() as cur:
        cur.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '%s');" % username)
        cur_response = cur.fetchone()
        user_exists = cur_response.items()[0][1]
        if user_exists:
            user_conflict_json = json.dumps({'error': 'Username is already taken.\n'})
            return user_conflict_json, 409
        else:
            if password == confirm_password:
                password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur.execute("CREATE USER '%s'@'%s' IDENTIFIED BY '%s';" % (username, env['host'], hashed_password))
                return json.dumps({}), 201
            else:
                passwords_dont_match_json = json.dumps({'error': 'Passwords do not match.\n'})
                return passwords_dont_match_json, 409
