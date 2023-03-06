from flask import Flask, g, jsonify, render_template, request

from db import Database

app = Flask(__name__)

DATABASE_PATH = ''

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

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/forgot-password')
def forgot_password():
  return render_template('forgot-password.html')

@app.route('/reset-password')
def reset_password():
  return render_template('reset-password.html')

if __name__ == '__main__':
  app.run(host='localhost', port=8080, debug=True)
