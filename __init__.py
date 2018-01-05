from flask import Flask, render_template, flash, url_for, redirect, request, g, session

from content_managment import Content
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart

from dbconnect import connection
import gc

TOPIC_DICT = Content()


app = Flask(__name__)
app.secret_key = 'uyotyfyfyytyftfty'
keyword = "password"

@app.route("/")
def homepage():
    return render_template("main.html")
    
@app.route("/dashbord/")
def dashbord():
	return render_template("dashbord.html", TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
	return render_template("405.html")	

@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
	
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashbord'))
				
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        # flash(e)
        return render_template("login.html", error = error)  

class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email    = TextField('Email Adress', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.required(), 
										  validators.EqualTo('confirm', message='Passwords must match.')])
	confirm  = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/" Terms of Service </a> and <href="/privacy/">Privacy Notice </a>(updated Jan 05, 2018)', [validators.Required()])
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
        	username = form.username.data
        	email    = form.email.data
        	password = sha256_crypt.encrypt(str(form.password.data))
        	c , conn = connection()

        	x = c.execute("SELECT * FROM users WHERE username = (%s)",
        					(thwart(username)))


        	if int(len(x)) > 0:
        		flash("That username is already taken, please choose anather")
        		return render_template('register.html', form=form)

        	else:
        		c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
        					(thwart(username), thwart(password), thwart(email), thwart("/introdution-to-python-programming/")))	

        		conn.commit()
        		flash("Thanks for registering !")
        		c.close()
        		conn.close()
        		gc.collect()


        		session['logged_in'] = True
        		session["username"] = username

        		return redirect(url_for('dashbord'))

        return render_template('register.html')	

    except Exception as e:
        return(str(e))





if __name__ == "__main__":
    app.run()
