from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_recaptcha import ReCaptcha
from markupsafe import Markup
import mysql.connector
import os

from chatbot import chatbot  # Assuming chatbot is correctly implemented in chatbot.py

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.static_folder = 'static'

# Google reCAPTCHA keys
app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6Lc6wxUqAAAAAM2NTB_5GaT7VCpduk8OcpBJwB2D",
    RECAPTCHA_SECRET_KEY="6Lc6wxUqAAAAAM-_TzbkUcLN4JYBjKoaQNa6H2GY"
))

recaptcha = ReCaptcha(app)

# Database connectivity
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='Srinu1204.',
    database='register'
)
cur = conn.cursor()

# Routes

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cur.fetchall()

    if len(users) > 0:
        session['id'] = users[0][0]
        flash('You were successfully logged in', 'success')
        return redirect('/index')
    else:
        flash('Invalid credentials !!!', 'danger')
        return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cur.execute("""INSERT INTO users(name,email,password) VALUES('{}','{}','{}')""".format(name, email, password))
    conn.commit()

    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cur.fetchall()

    flash('You have successfully registered!', 'success')
    session['id'] = myuser[0][0]
    return redirect('/index')

@app.route('/suggestion', methods=['POST'])
def suggestion():
    email = request.form.get('uemail')
    suggesMess = request.form.get('message')

    cur.execute("""INSERT INTO suggestion(email,message) VALUES('{}','{}')""".format(email, suggesMess))
    conn.commit()

    flash('Your suggestion was successfully sent!', 'success')
    return redirect('/index')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run(debug=True)
