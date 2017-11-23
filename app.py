from flask import Flask
from flask import render_template

import config
import controllers
from extensions import login_manager

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Passenger expects to find an object called application
application = app

# Register the controllers
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.sqlpage)
app.register_blueprint(controllers.info)
app.register_blueprint(controllers.pattern)
app.register_blueprint(controllers.upload)
# app.register_blueprint(controllers.database)
app.register_blueprint(controllers.allsamples)
app.register_blueprint(controllers.ourTeam)
app.register_blueprint(controllers.new_user)
app.register_blueprint(controllers.login)

login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

app.secret_key = config.secret_key

#sys.stderr = open("error_log", "a")

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
