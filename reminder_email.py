from flask import (Flask, g, jsonify, redirect, render_template, request, session)
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from run import app, get_db, mail
from datetime import date, datetime, timedelta

subject = 'Vaccine Reminder'
sender='vaccinationreminder2023@gmail.com'

def send_reminder_email():
    with app.app_context():
        users = get_db().get_users()
        if users:
            for user in users:
                todayDate = datetime.strptime(datetime.strftime(datetime.today(), "%d/%m/%Y"), "%d/%m/%Y")
                birthDate = datetime.strptime(user['birthdate'], "%d/%m/%Y")
                if (todayDate == birthDate + timedelta(days=41)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=42), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'HEP B Vaccine - Dose 2\n'
                    + 'OPV Vaccine - Dose 2\n'
                    + 'DPT Vaccine - Dose 1\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=44)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=45), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'IPV Vaccine - Dose 1\n'
                    + 'PNEUMOCOCCAL Vaccine - Dose 1\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=59)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=60), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'ROTAVIRUS Vaccine - Dose 1\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=69)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=70), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'OPV Vaccine - Dose 3\n'
                    + 'DPT Vaccine - Dose 2\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=75)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=76), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'IPV Vaccine - Dose 2\n'
                    + 'PNEUMOCOCCAL Vaccine - Dose 2\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=97)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=98), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'OPV Vaccine - Dose 4\n'
                    + 'DPT Vaccine - Dose 3\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=106)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=107), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'IPV Vaccine - Dose 3\n'
                    + 'PNEUMOCOCCAL Vaccine - Dose 3\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=119)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=120), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'HIB Vaccine - Dose 1\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=144)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=145), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'ROTAVIRUS Vaccine - Dose 2\n'
                    mail.send(msg)
                if (todayDate == birthDate + timedelta(days=154)):
                    msg = Message(subject=subject, sender=sender, recipients=[user['email']])
                    msg.body = 'Dear Parents,\nOn '+ datetime.strftime(birthDate + timedelta(days=155), "%d/%m/%Y")
                    + ' or tomorrow your child, '+ user['name'] +' should be vaccinate using following vaccines.\n'
                    + 'OPV Vaccine - Dose 5\n'
                    mail.send(msg)

send_reminder_email()

# scheduler = BackgroundScheduler()
# scheduler.add_job(send_reminder_email, trigger='cron', hour='6', minute='00')
# scheduler.start()
