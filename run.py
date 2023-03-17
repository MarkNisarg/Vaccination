from flask import (Flask, g, jsonify, redirect, render_template, request, session, flash)
from passlib.hash import pbkdf2_sha256
from flask_mail import Mail, Message
from random import randint
from datetime import date, datetime, timedelta

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
                elif user is None:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif email and not typed_password:
            message = "Missing password, please try again"
        elif not email and typed_password:
            message = "Missing email, please try again"
            # render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    message = None
    if request.method == 'POST':
        form_otp = request.form['digit1'] + request.form['digit2'] + request.form['digit3'] + request.form['digit4'] + \
                   request.form['digit5'] + request.form['digit6']
        if form_otp and get_db().get_otp(session['email']):
            get_db().update_verify(session['email'])
            session.pop('user', None)
            return redirect('/login')
        else:
            message = "Incorrect otp! try again."
            return render_template('/otp_verification.html')
    return render_template('/otp_verification.html')


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
            get_db().create_vaccine_schedule(email, phone)
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
            return redirect('/login')
    return render_template('reset-password.html')


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


def get_vaccine_dates(dateFormat):
    vaccineDates = []
    dateOfBirth = datetime.strptime(session['user']['birthdate'], "%d/%m/%Y")
    vaccineDates.append(datetime.strftime(dateOfBirth, dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=42), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=45), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=60), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=70), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=76), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=98), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=107), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=120), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=145), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=155), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=180), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=240), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=275), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=365), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=400), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=500), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=545), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=610), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=665), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=730), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=1825), dateFormat))
    vaccineDates.append(datetime.strftime(dateOfBirth + timedelta(days=3650), dateFormat))
    return vaccineDates


# A GET request to return all vaccine dates.
@app.route('/api/get_vaccine_dates', methods=['GET'])
def get_vaccinations_dates():
    return get_vaccine_dates('%d/%m/%Y')


@app.route('/api/update_vaccine_status', methods=['POST'])
def update_vaccination_status():
    vaccine = request.form.get('vaccine')
    status = request.form.get('status')
    get_db().update_vaccine_status(vaccine, status, session['user']['email'])
    return redirect('/vaccine-schedule')


# A GET request to return all vaccine status.
@app.route('/api/get_vaccine_status', methods=['GET'])
def get_vaccinations_status():
    vaccinesStatus = get_db().get_vaccines_status(session['user']['email'])
    return jsonify(vaccinesStatus)


@app.route('/vaccine-schedule')
def vaccine_schedule():
    if 'user' in session:
        vaccineDates = get_vaccine_dates("%d/%m/%Y")
        return render_template('vaccine-schedule.html', header='Vaccine Schedule', vaccineDates=vaccineDates)
    else:
        return redirect('/login')


@app.route('/calendar-schedule')
def calendar_schedule():
    if 'user' in session:
        today = date.today().strftime("%d %B, %Y")
        vaccineDates = get_vaccine_dates("%d %B, %Y")
        return render_template('calendar-schedule.html', header='Calendar Schedule', vaccineDates=vaccineDates,
                               today=today)
    else:
        return redirect('/login')


@app.route('/vaccine-details')
def vaccine_details():
    if 'user' in session:
        return render_template('vaccine-details.html', header='Vaccine Details')
    else:
        return redirect('/login')


@app.route('/vaccine-details/bcg-vaccine')
def bcg_vaccine():
    if 'user' in session:
        return render_template('bcg-vaccine.html', header='BCG Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/polio-vaccine')
def polio_vaccine():
    if 'user' in session:
        return render_template('polio-vaccine.html', header='Polio Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/hepatitis-a-vaccine')
def hepatitis_a_vaccine():
    if 'user' in session:
        return render_template('hepatitis-a-vaccine.html', header='Hepatitis A Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/hepatitis-b-vaccine')
def hepatitis_b_vaccine():
    if 'user' in session:
        return render_template('hepatitis-b-vaccine.html', header='Hepatitis B Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/dpt-vaccine')
def dpt_vaccine():
    if 'user' in session:
        return render_template('dpt-vaccine.html', header='DPT Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/hib-vaccine')
def hib_vaccine():
    if 'user' in session:
        return render_template('hib-vaccine.html', header='HIB Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/chickenpox-vaccine')
def chickenpox_vaccine():
    if 'user' in session:
        return render_template('chickenpox-vaccine.html', header='Chickenpox Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/measles-vaccine')
def measles_vaccine():
    if 'user' in session:
        return render_template('measles-vaccine.html', header='Measles Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/mmr-vaccine')
def mmr_vaccine():
    if 'user' in session:
        return render_template('mmr-vaccine.html', header='MMR Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/rotavirus-vaccine')
def rotavirus_vaccine():
    if 'user' in session:
        return render_template('rotavirus-vaccine.html', header='Rotavirus Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/typhoid-vaccine')
def typhoid_vaccine():
    if 'user' in session:
        return render_template('typhoid-vaccine.html', header='Typhoid Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/pneumococcal-vaccine')
def pneumococcal_vaccine():
    if 'user' in session:
        return render_template('typhoid-vaccine.html', header='Pneumococcal Vaccine')
    else:
        return redirect('/login')


@app.route('/vaccine-details/tetanus-toxoid-vaccine')
def tetanus_toxoid_vaccine():
    if 'user' in session:
        return render_template('tetanus-toxoid-vaccine.html', header='Tetanus Toxoid Vaccine')
    else:
        return redirect('/login')


@app.route('/ask-question', methods=['POST', 'GET'])
def ask_question():
    if 'user' in session:
        if request.method == 'POST':
            if 'question' in request.form:
                question = request.form['question']
                if question:
                    user = get_db().get_user(session['user']['email'])
                    if user:
                        mail1 = Mail(app)
                        get_db().update_ask_tbl(user['email'], user['contact'], question)
                        msg = Message(subject='Question raised by patient', sender='vaccinationreminder2023@gmail.com',
                                      recipients=["doctoratvaccinereminder@gmail.com"])
                        msg.body = str("Dear Doctor,\n\nYou have received a new question from " + user[
                            'name'] + ".\n\nQuestion:" + question + "\n\nContact Details:\nName: " + user[
                                           'name'] + "\nEmail: " + user['email'] + "\nPhone:" + user['contact'])
                        # get_db().update_otp(otp, email)
                        mail1.send(msg)
                        flash('You question was successfully sent to doctor!')
        return render_template('ask-question.html', header='Ask Question')
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
