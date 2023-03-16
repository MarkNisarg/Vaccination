from flask import (Flask, g, jsonify, redirect, render_template, request, session)
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail, Message
from random import randint
from datetime import datetime, timedelta

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
otp = randint(100000, 999999)


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
            if email == user['email']:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    return redirect('/vaccine-schedule')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif email and not typed_password:
            message = "Missing password, please try again"
        elif not email and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    print (otp)
    if request.method == 'POST':
        print('Hello nisarg')
        form_otp = request.form['digit1'] + request.form['digit2'] + request.form['digit3'] + request.form['digit4'] + request.form['digit5'] + request.form['digit6']
        if form_otp and get_db().get_otp(session['email']):
            get_db().update_verify(session['email'])
            session.pop('user', None)
            return redirect('/login')
    return render_template('/otp_verification.html')


# @app.route('/validate', methods=['POST'])
# def validate():
#     email = session['email']
#     user_otp = request.form.get('user_otp')
#     # print(email)
#     db_otp = get_db().get_otp(email)
#     # print(db_otp)
#     if db_otp == int(user_otp):
#         # print(db_otp)
#         print("successful")
#         get_db().update_verify(email)
#         return render_template('/contact.html')
#     return "<h2>not successful</h2>"


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
            msg = Message(subject='OTP', sender='vaccinationreminder2023@gmail.com', recipients=[email])
            msg.body = str(otp)
            get_db().update_otp(otp, email)
            mail.send(msg)
            return redirect('/verify')
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


# @app.route('/otp_verification')
# def otp_verification():
#     return render_template('otp_verification.html')


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

@app.route('/vaccine-schedule')
def vaccine_schedule():
    if 'user' in session:
      vaccineDates = []
      dateOfBirth = datetime.strptime(session['user']['birthdate'], "%d/%m/%Y")
      vaccineDates.append(datetime.strftime(dateOfBirth, "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=42), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=45), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=60), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=70), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=76), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=98), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=107), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=120), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=145), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=155), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=180), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=240), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=275), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=365), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=400), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=500), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=545), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=610), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=665), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=730), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=1825), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=3650), "%d/%m/%Y"))
      return render_template('vaccine-schedule.html', header = 'Vaccine Schedule', vaccineDates = vaccineDates)
    else:
      return redirect('/login')

@app.route('/calendar-schedule')
def calendar_schedule():
    if 'user' in session:
      vaccineDates = []
      dateOfBirth = datetime.strptime(session['user']['birthdate'], "%d/%m/%Y")
      vaccineDates.append(datetime.strftime(dateOfBirth, "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=42), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=45), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=60), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=70), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=76), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=98), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=107), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=120), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=145), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=155), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=180), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=240), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=275), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=365), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=400), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=500), "%d/%m/%Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=545), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=610), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=665), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=730), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=1825), "%d %B, %Y"))
      vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=3650), "%d %B, %Y"))
      return render_template('calendar-schedule.html', header = 'Calendar Schedule', vaccineDates = vaccineDates)
    else:
      return redirect('/login')

@app.route('/vaccine-details')
def vaccine_details():
    if 'user' in session:
      return render_template('vaccine-details.html', header = 'Vaccine Details')
    else:
      return redirect('/login')

@app.route('/vaccine-details/bcg-vaccine')
def bcg_vaccine():
    if 'user' in session:
      return render_template('bcg-vaccine.html', header = 'BCG Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/polio-vaccine')
def polio_vaccine():
    if 'user' in session:
      return render_template('polio-vaccine.html', header = 'Polio Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/hepatitis-a-vaccine')
def hepatitis_a_vaccine():
    if 'user' in session:
      return render_template('hepatitis-a-vaccine.html', header = 'Hepatitis A Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/hepatitis-b-vaccine')
def hepatitis_b_vaccine():
    if 'user' in session:
      return render_template('hepatitis-b-vaccine.html', header = 'Hepatitis B Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/dpt-vaccine')
def dpt_vaccine():
    if 'user' in session:
      return render_template('dpt-vaccine.html', header = 'DPT Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/hib-vaccine')
def hib_vaccine():
    if 'user' in session:
      return render_template('hib-vaccine.html', header = 'HIB Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/chickenpox-vaccine')
def chickenpox_vaccine():
    if 'user' in session:
      return render_template('chickenpox-vaccine.html', header = 'Chickenpox Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/measles-vaccine')
def measles_vaccine():
    if 'user' in session:
      return render_template('measles-vaccine.html', header = 'Measles Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/mmr-vaccine')
def mmr_vaccine():
    if 'user' in session:
      return render_template('mmr-vaccine.html', header = 'MMR Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/rotavirus-vaccine')
def rotavirus_vaccine():
    if 'user' in session:
      return render_template('rotavirus-vaccine.html', header = 'Rotavirus Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/typhoid-vaccine')
def typhoid_vaccine():
    if 'user' in session:
      return render_template('typhoid-vaccine.html', header = 'Typhoid Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/pneumococcal-vaccine')
def pneumococcal_vaccine():
    if 'user' in session:
      return render_template('typhoid-vaccine.html', header = 'Pneumococcal Vaccine')
    else:
      return redirect('/login')

@app.route('/vaccine-details/tetanus-toxoid-vaccine')
def tetanus_toxoid_vaccine():
    if 'user' in session:
      return render_template('tetanus-toxoid-vaccine.html', header = 'Tetanus Toxoid Vaccine')
    else:
      return redirect('/login')

@app.route('/ask-question')
def ask_question():
    if 'user' in session:
      return render_template('ask-question.html', header = 'Ask Question')
    else:
      return redirect('/login')

@app.route('/profile', methods=['POST', 'GET'])
def profile_question():
    if 'user' in session:
      if request.method == 'POST':
        if 'name' in request.form:
          name = request.form['name']
          if name:
           get_db().update_name(request.form['name'], session['user']['email'])
           session['user']['name'] = name
        if 'dob' in request.form:
          dob = request.form['dob']
          if dob:
           get_db().update_dob(dob, session['user']['email'])
           session['user']['birthdate'] = dob
        if 'contact' in request.form:
          contact = request.form['contact']
          if contact:
           get_db().update_phone(contact, session['user']['email'])
           session['user']['contact'] = contact
        if 'currentpassword' in request.form and 'newpassword' in request.form and 'confirmnewpassword' in request.form:
          currentpassword = request.form['currentpassword']
          newpassword = request.form['newpassword']
          confirmnewpassword = request.form['confirmnewpassword']
          if currentpassword and newpassword and confirmnewpassword:
            if pbkdf2_sha256.verify(currentpassword, session['user']['encrypted_password']):
              encrypted_password = pbkdf2_sha256.hash(newpassword)
              get_db().update_password(newpassword, encrypted_password)
              session['user']['password'] = encrypted_password
        session.modified = True
      return render_template('profile.html', header='Profile')
    else:
      return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='localhost', port=8082, debug=True)
