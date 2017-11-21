import MySQLdb
import MySQLdb.cursors

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
