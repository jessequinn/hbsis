from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import urllib.request, json

app = Flask(__name__)

app.secret_key = "secret key"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    with urllib.request.urlopen('http://localhost:5050/countries') as url:
        data = json.loads(url.read().decode())

        error = None
        if request.method == 'POST':
            if request.form['city'] != '':
                with urllib.request.urlopen('http://localhost:5050/'+request.form['country'].upper()+'/'+request.form['city'].capitalize()) as url:
                    ids = json.loads(url.read().decode())

                if not ids['data']:
                    error = 'No data exists for '+request.form['city'].capitalize()+'!'
                    return render_template('index.html', countries=data['data'], error=error)
                else:
                    flash(ids)
                    return redirect(url_for('home'))
            else:
                error = 'Enter a city name!'

    return render_template('index.html', countries=data['data'], error=error)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
