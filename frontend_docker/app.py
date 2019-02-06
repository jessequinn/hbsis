import datetime
import json
import pytz
import urllib.request
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from pytz import timezone
# import tzlocal

app = Flask(__name__)
bcrypt = Bcrypt(app) # password hashing

# set environmental variable to development or production class
app.config.from_object(os.environ['APP_MODE'])


db = SQLAlchemy(app)

# import db schema
from models import *

def datetimefilter(value, format="%A"):
    '''
    Datetime filter for Jinja. Formats date to US/Eastern from the UTC value.

    :param value: input value
    :param format: format of return date. default day of week.
    :return: formatted date
    '''

    value = datetime.datetime.fromtimestamp(value)
    tz = pytz.timezone('US/Eastern')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


app.jinja_env.filters['datetimefilter'] = datetimefilter


def login_required(f):
    '''
    Wrapper for login

    :param f: function to wrap
    :return: wrap object
    '''

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
    '''
    Main page after login. Contains a search form for city weather forecast.

    :return: rendered template
    '''

    # session.clear()
    registrations = db.session.query(WeatherRegistration).all()
    print(registrations)

    if 'city_ids' not in session:
        session['city_ids'] = []

    with urllib.request.urlopen('http://localhost:5050/countries') as url:
        data = json.loads(url.read().decode())

        error = None
        if request.method == 'POST':
            if request.form['city'] != '':
                with urllib.request.urlopen(
                        'http://localhost:5050/' + request.form['country'].upper() + '/' + request.form[
                            'city'].capitalize()) as url:
                    ids = json.loads(url.read().decode())

                if not ids['data']:
                    error = 'No data exists for ' + request.form['city'].capitalize() + '!'
                    return render_template('index.html', countries=data['data'], error=error)
                else:
                    city_ids = session['city_ids']

                    if any(ids['data'][0]['id'] in c for c in city_ids):
                        flash('City has already been registered')
                    else:
                        city_ids.append([request.form['city'], ids['data'][0]['id']])
                    session['city_ids'] = city_ids

                    return redirect(url_for('home'))
            else:
                error = 'Enter a city name!'

    return render_template('index.html', countries=data['data'], error=error)


@app.route('/forecast<id>')
@login_required
def forecast(id):
    '''
    5 day forecast page.

    :param id: city id
    :return: rendered template
    '''

    with urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/forecast/daily?id=' + id + '&cnt=5&APPID=eb8b1a9405e659b2ffc78f0a520b1a46&units=metric') as url:
        data = json.loads(url.read().decode())

    return render_template('forecast.html', data=data)


@app.route('/remove<id>')
@login_required
def remove(id):
    '''
    Function simply removes city from list of cities.

    :param id: city id
    :return: rendered template
    '''

    for c in session['city_ids']:
        if int(id) == c[1]:
            session['city_ids'].remove(c)
            session.modified = True

    return redirect(url_for('home'))


@app.route('/welcome')
def welcome():
    '''
    Generic welcome page.

    :return: rendered template
    '''
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page.
    :return:
    '''

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
    '''
    Logout page.

    :return: rendered template
    '''
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run()
