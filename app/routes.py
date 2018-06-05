from app import app
from app.forms import LoginForm
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse



@app.route('/') # change '/' to actual home WHEN exists(actual home)
@app.route('/blog')
def index():

    user = {'username': 'admin'}

    posts = [
        {
            'author': {'username': 'Kvarjo'},
            'body': 'Riktigt najs idag'
        },
        {
            'author': {'username': 'Admin'},
            'body': 'jag håller med @Kvarjo'
        }

    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    # store form data
    form = LoginForm()

    # get user data from database if form is filled out correctly
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # check username and password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user)

        # check for next in URL, else sets redirect to admin page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# admin page
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title="Secret Area")
