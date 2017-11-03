from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import hash

login = Blueprint('login', __name__, template_folder='templates')

db = extensions.connect_to_database()

@login.route('/login', methods = ['GET', 'POST'])
def login_route():
    options = {
        "isUsernameEmpty": False,
        "isPasswordEmpty": False,
        "isUsernameWrong": False,
        "isPassowrdWrong": False
    }
    if request.method == 'POST':
        username = request.form['username']
        passwordLogin = request.form['password']
        
        if username == '' or passwordLogin == '':
            if username == '':
                options['isUsernameEmpty'] = True
            if passwordLogin == '':
                options['isPasswordEmpty'] = True
            return render_template("login.html", **options)
        
        cur1 = db.cursor()
        cur1.execute('SELECT username FROM UserInfo')
        results1 = cur1.fetchall()
        same = 0
        for user in results1:
            if user['username'] == username:
                same += 1
        if same == 0:
            options['isUsernameWrong'] = True
        if options['isUsernameWrong']:
            return render_template("login.html", **options)
        
        
        cur2 = db.cursor()
        cur2.execute('SELECT password FROM UserInfo WHERE username = %s', (username, ))
        results2 = cur2.fetchall()
        for password in results2:
            salt = hash.getSalt(password['password'])
            hashPassword = hash.hashPasswordWithSalt(passwordLogin, salt)

            if password['password'] != hashPassword:
                options['isPassowrdWrong'] = True
        if options['isPassowrdWrong']:
            return render_template("login.html", **options)

        if 'username' in session:
            session.pop('username', None)
        
        session['username'] = username
        return redirect(url_for('main.main_route'))
        
    return render_template("login.html")

  


