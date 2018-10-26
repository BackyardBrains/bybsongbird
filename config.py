# Do NOT commit this file to github
# Make a seperate one for your deployed environment
import os
env = dict(
        host = '0.0.0.0',
        port = 3000,
        user = 'bybsongbird',
        password = 'FW@n{rb1CctMZ9',
        db = 'bybsongbird',
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'static', 'songs', 'users'),
        debug = False
)

secret_key = '55238919ae0b573b34c9986034c27279'
host = env['host']
port = env['port']
user = env['user']
passwd = env['password']
database = env['db']
