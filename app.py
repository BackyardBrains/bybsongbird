from flask import Flask
<<<<<<< HEAD

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
=======
from flask import render_template
import extensions
import api.api_blueprint
import api.apiPath
import api.apiUpload
import config
import controllers
import sys
#sys.path.append("./api")


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
app.register_blueprint(controllers.database)
app.register_blueprint(controllers.allsamples)
app.register_blueprint(controllers.ourTeam)
app.register_blueprint(controllers.new_user)
app.register_blueprint(controllers.login)

#API urls
app.register_blueprint(api.api_blueprint.api_blueprint)
app.register_blueprint(api.apiPath.apiPath)
app.register_blueprint(api.apiUpload.apiUpload)

extensions.login_manager.init_app(app)


@extensions.login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')


app.secret_key = config.secret_key

# sys.stderr = open("error_log", "a")

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=config.env['debug'])
>>>>>>> c71ef71d50b6404c3ce11561f7b56354609da266
