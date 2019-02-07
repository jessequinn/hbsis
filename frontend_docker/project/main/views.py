import datetime
import json
import pytz
import urllib.request
from flask import render_template, request, flash, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from project import app, db
from project.models import WeatherRegistration
from .forms import WeatherRegistrationForm

main_blueprint = Blueprint(
    'main', __name__,
    template_folder='templates'
)


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


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    '''
    Main page after login. Contains a search form for city weather forecast.

    :return: rendered template
    '''

    weatherRegistrations = db.session.query(WeatherRegistration).filter_by(user_id=current_user.id).all()

    with urllib.request.urlopen('http://localhost:5050/countries') as url:
        data = json.loads(url.read().decode())

    error = None
    form = WeatherRegistrationForm(request.form)
    form.country.choices = [(c, c) for c in data['data']]  # dyanmically produce countries

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.city.data != '':
                with urllib.request.urlopen(
                        'http://localhost:5050/' + form.country.data.upper() + '/' + form.city.data.capitalize()) as url:
                    ids = json.loads(url.read().decode())

                if not ids['data']:
                    error = 'No data exists for ' + form.city.data.capitalize() + '!'
                    return render_template('index.html', form=form, error=error, user=current_user, weatherRegistrations=weatherRegistrations)
                else:
                    if any(ids['data'][0]['id'] == wr.city_id for wr in weatherRegistrations):
                        error = form.city.data.capitalize() + ' has already been registered.'
                        return render_template('index.html', form=form, error=error, user=current_user,
                                               weatherRegistrations=weatherRegistrations)
                    else:
                        new_weatherregistration = WeatherRegistration(form.city.data, ids['data'][0]['id'],
                                                                      form.country.data, current_user.id)
                        db.session.add(new_weatherregistration)

                        failed = False
                        try:
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            db.session.flush()
                            failed = True
                            print(e)

                        if failed:
                            error = 'Error with registration.'
                            return render_template('index.html', form=form, error=error, user=current_user,
                                                   weatherRegistrations=weatherRegistrations)
                        else:
                            flash(form.city.data.capitalize() + ' was registered successfully.')
                            return redirect(url_for('main.home'))
            else:
                error = 'Enter a city name!'

    return render_template('index.html', form=form, error=error, user=current_user,
                           weatherRegistrations=weatherRegistrations)


@main_blueprint.route('/forecast<id>')
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


@main_blueprint.route('/remove<id>')
@login_required
def remove(id):
    '''
    Function simply removes city from list of cities.

    :param id: city id
    :return: rendered template
    '''

    with urllib.request.urlopen('http://localhost:5050/countries') as url:
        data = json.loads(url.read().decode())

    form = WeatherRegistrationForm(request.form)
    form.country.choices = [(c, c) for c in data['data']]  # dyanmically produce countries

    db.session.query(WeatherRegistration).filter_by(id=id).delete()

    failed = False
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        failed = True
        print(e)

    if failed:
        error = 'Could not remove registration.'
        weatherRegistrations = db.session.query(WeatherRegistration).filter_by(user_id=current_user.id).all()
        return render_template('index.html', form=form, error=error, user=current_user,
                               weatherRegistrations=weatherRegistrations)
    else:
        flash('Registration was removed successfully.')
        return redirect(url_for('main.home'))
