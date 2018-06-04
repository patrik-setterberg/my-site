from app import app
from app.forms import LoginForm
from flask import flash, redirect, render_template


@app.route('/')
@app.route('/index')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)
