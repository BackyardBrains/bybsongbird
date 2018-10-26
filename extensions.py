import MySQLdb
import MySQLdb.cursors
from flask_login import UserMixin
from flask_login import login_manager as lm

import config


def connect_to_database(user=0, password=0):
    if not user:
        user = config.env['user']
    if not password:
        password = config.env['password']
    options = {
        'host': config.env['host'],
        'user': user,
        'passwd': password,
        'db': config.env['db'],
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    db = MySQLdb.connect(**options)
    db.autocommit(True)
    return db


class User(UserMixin):
    def __init__(self, username):
        self.id = username


lm.session_protection = "strong"
login_manager = lm.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
