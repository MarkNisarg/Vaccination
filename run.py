from flask import (Flask, g, jsonify, redirect, render_template, request,
                   session)
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail, Message
from random import randint

from db import Database

app = Flask(__name__)
mail = Mail(app)
app.secret_key = b'demokeynotreal!'
DATABASE_PATH = 'vaccination.sqlite3'
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'vaccinationreminder2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'lqzcijqlsoqzyqtu'  # you have to give your password of gmail account
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Message = request.form['Message']
        get_db().update_contact(Name, Email, Message)
    return render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        typed_password = request.form.get('password')
        if email and typed_password:
            user = get_db().get_user(email)
            if email == user['username']:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    print("Hi bro")
                    session['email'] = user
                    return redirect('/contact')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif email and not typed_password:
            message = "Missing password, please try again"
        elif not email and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)


@app.route('/verify')
def verify(email):
    # email = request.form['email']
    msg = Message(subject='OTP', sender='vaccinationreminder2023@gmail.com', recipients=[email])
    msg.body = str(otp)
    get_db().update_otp(otp, email)
    mail.send(msg)
    return render_template('/otp_verification.html')


@app.route('/validate', methods=['POST'])
def validate():
    email = session['email']
    user_otp = request.form.get('user_otp')
    # print(email)
    db_otp = get_db().get_otp(email)
    # print(db_otp)
    if db_otp == int(user_otp):
        # print(db_otp)
        print("successful")
        get_db().update_verify(email)
        return render_template('/contact.html')
    return "<h2>not successful</h2>"


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm password']
        phone = request.form['phone']
        birthday = request.form['birthday']
        if password != confirmPassword:
            error_msg = "Passwords do not match."
            return render_template('signup.html', error_msg=error_msg)
        elif name and email and password:
            encrypted_password = pbkdf2_sha256.hash(password)
            get_db().update_signup(name, email, encrypted_password, phone, birthday)
            session['email'] = email
            return verify(email)
    return render_template('signup.html')


@app.route('/forgot-password')
def forgot_password():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm password']
        if password != confirmPassword:
            error_msg = "Passwords do not match."
            return render_template('reset-password.html', error_msg=error_msg)
        elif email and password:
            encrypted_password = pbkdf2_sha256.hash(password)
            get_db().update_password(email, encrypted_password)
            session['email'] = email
            return render_template('/contact.html')
    return render_template('reset-password.html')


@app.route('/otp_verification')
def otp_verification():
    return render_template('otp_verification.html')


@app.route('/reset-password', methods=['POST', 'GET'])
def reset_password():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm password']
        if password != confirmPassword:
            error_msg = "Passwords do not match."
            return render_template('reset-password.html', error_msg=error_msg)
        elif email and password:
            encrypted_password = pbkdf2_sha256.hash(password)
            get_db().update_password(email, encrypted_password)
            session['email'] = email
            return render_template('/contact.html')
    return render_template('reset-password.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8082, debug=True)
