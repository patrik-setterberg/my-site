from app import app, db
from app.forms import LoginForm, BlogPostForm, BlogCommentForm, DeletePostForm
from app.models import User, BlogPost, BlogComment
from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])  # change '/' to actual home
@app.route('/blog', methods=['GET', 'POST'])
def index():

    form = BlogCommentForm()

    # POST
    if form.validate_on_submit():

        comment = BlogComment(author=form.comment_author.data,
                              body=form.comment_body.data, email=form.
                              comment_email.data, post_id=form.post_id.data)

        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been submitted. Thank you!')
        return redirect(url_for('index'))

    # GET
    # retrieve posts and comments from database
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    comments = BlogComment.query.all()

    return render_template('index.html', title='Home', posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form,
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


# manage blog
@app.route('/manage_blog', methods=['GET', 'POST'])
@login_required
def manage_blog():

    form = BlogPostForm()

    if form.validate_on_submit():

        post = BlogPost(title=form.post_title.data, body=form.post_body.data)

        db.session.add(post)
        db.session.commit()

        flash('Post is now live!')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).paginate(
        page, app.config['TITLES_PER_PAGE'], False)
    next_url = url_for('manage_blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('manage_blog', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('manage_blog.html', title='Manage Blog',
                           form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


# edit blog post
@app.route('/edit_blog_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):

    form = BlogPostForm()
    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()

    if form.validate_on_submit():
        post.title = form.post_title.data
        post.body = form.post_body.data
        post.last_edit = datetime.utcnow()
        db.session.commit()

        flash('Changes saved.')
        return redirect(url_for('manage_blog'))

    elif request.method == 'GET':
        form.post_title.data = post.title
        form.post_body.data = post.body

    return render_template('edit_blog_post.html', form=form, post=post)


# delete blog post
@app.route('/delete_post/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    form = DeletePostForm()
    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        flash('Post deleted successfully.')
        return redirect(url_for('manage_blog'))

    return render_template('delete_post.html', form=form, post=post)
