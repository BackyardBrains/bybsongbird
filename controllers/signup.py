from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
import MySQLdb
import MySQLdb.cursors
from extensions import *
import config
import hash

signup = Blueprint('signup', __name__, template_folder='templates')

db = connect_to_database()

@signup.route('/signup', methods = ['GET', 'POST'])
def signup_route():
    if 'username' in session:
        return redirect(url_for('main.main_route'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        
        isUsernameRepeated = False
        isPassword1TooShort = False
        isPassword12Mismatch = False
        
        cur1 = db.cursor()
        cur1.execute('SELECT username FROM UserInfo')
        result1 = cur1.fetchall()
        for user in result1:
            if user['username'] == username:
                isUsernameRepeated = True
                
        if not password1 == password2:
            isPassword12Mismatch = True

        if isStrLengthLessThanN(password1, 7):
            isPassword1TooShort = True
        
        options = {
            "edit" :False,
            "method" :'POST',
            "isUsernameRepeated": isUsernameRepeated,
            "isPassword1TooShort": isPassword1TooShort,
            "isPassword12Mismatch": isPassword12Mismatch
        }
        for key in options:
            if options[key] == True:
                return render_template("signup.html", **options)
        
        hashPassword = hash.hashPassword(password1)
        
        cur2 = db.cursor()
        add_user = ("INSERT INTO UserInfo (username, password, email) VALUES (%s, %s, %s)")
        data_user = (username, hashPassword, email)
        cur2.execute(add_user, data_user)
        return redirect(url_for('login.login_route'))
    
    options = {
        "edit" : False,
        "method" : 'GET'     
    }
    return render_template("signup.html", **options)    