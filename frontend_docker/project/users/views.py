from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import login_user, logout_user, login_required
from project.users.forms import LoginForm
from project.models import User, bcrypt

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('You are logged in.')
                return redirect(url_for('main.home'))
            else:
                error = 'Invalid log in credentials. Please try again.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('main.welcome'))
