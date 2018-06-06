from app import app, db
from app.forms import LoginForm, BlogPostForm, BlogCommentForm
from app.models import User, BlogPost, BlogComment
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route('/')  # change '/' to actual home WHEN exists(actual home)
@app.route('/blog')
def index():

    form = BlogCommentForm()

    if form.validate_on_submit():

        comment = BlogComment(author=form.comment_author.data,
            body=form.comment_body.data, email=form.comment_email.data)

        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been submitted. Thank you!')
        return redirect(url_for('/blog'))

    posts = BlogPost.query.all()
    comments = BlogComment.query.all()

    return render_template('index.html', title='Home', posts=posts, form=form,
        comments=comments)


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
    return render_template('admin.html', title='Secret Area')


# new blog post (rename to manage blog)
@app.route('/new_blog_post', methods=['GET', 'POST'])
@login_required
def new_blog_post():

    form = BlogPostForm()

    if form.validate_on_submit():

        post = BlogPost(title=form.post_title.data, body=form.post_body.data)

        db.session.add(post)
        db.session.commit()

        flash('Post is now live!')
        return redirect(url_for('admin'))

    return render_template('new_blog_post.html', title='New Blog Post',
                           form=form)
