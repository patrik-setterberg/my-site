from app import app, db
from app.forms import LoginForm, BlogPostForm, BlogCommentForm, DeletePostForm
from app.forms import AddCategoryForm
from app.models import User, BlogPost, BlogComment, BlogCategory
from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


# home
@app.route('/', methods=['GET'])  # change '/' to actual home
@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


# portfolio
@app.route('/portfolio', methods=['GET'])
def portfolio():

    return render_template('portfolio.html')


# blog
@app.route('/blog', methods=['GET', 'POST'])
def blog():

    # retrieve posts and comments from database
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog', page=posts.prev_num) \
        if posts.has_prev else None

    comments = BlogComment.query.all()  # not particularly elegant

    return render_template('blog.html', title='Blog', posts=posts.items,
                           next_url=next_url, prev_url=prev_url,
                           comments=comments)


# browse blog posts by category
@app.route('/blog/cat/<category>', methods=['GET'])
def browse_cat(category):

    # retrieve category posts and comments from database
    page = request.args.get('page', 1, type=int)
    posts = (BlogPost.query.filter_by(category=category)
             .order_by(BlogPost.timestamp.desc())
             .paginate(page, app.config['POSTS_PER_PAGE'], False))
    next_url = url_for('blog/cat/<category>', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog/cat/<category>', page=posts.prev_num) \
        if posts.has_prev else None

    # NÅN TYP AV JOIN? GET COMMENTS FOR POSTS IN CATEGORY PLS
    comments = BlogComment.query.all()  # not particularly elegant

    return render_template('blog.html', title=('Blogposts in ' + category),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url, comments=comments)


# post page
@app.route('/blog/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):

    form = BlogCommentForm()
    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()
    comments = BlogComment.query.filter_by(post_id=int(post_id)).all()

    # POST
    if form.validate_on_submit():

        comment = BlogComment(author=form.comment_author.data,
                              body=form.comment_body.data,
                              email=form.comment_email.data,
                              post_id=int(form.post_id.data))

        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been submitted. Thank you!')
        return redirect(url_for('post', post_id=post.id, title=post.title))

    elif request.method == 'GET':
        form.post_id.data = post.id

    return render_template('post.html', form=form, post=post,
                           comments=comments, title=post.title)


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
@app.route('/admin/manage_blog', methods=['GET', 'POST'])
@login_required
def manage_blog():

    form = BlogPostForm()
    form.category.choices = ([(cat.category, cat.category) for cat in
                             BlogCategory.query.all()])

    # post new comment
    if form.validate_on_submit() and form.submit.data:

        post = BlogPost(title=form.post_title.data,
                        body=form.post_body.data,
                        category=form.category.data)

        db.session.add(post)
        db.session.commit()

        flash('Post is now live!')
        return redirect(url_for('blog'))

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
@app.route('/admin/edit_blog_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):

    form = BlogPostForm()
    form.category.choices = ([(cat.category, cat.category) for cat in
                             BlogCategory.query.all()])

    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()

    # update post data
    if form.validate_on_submit() and form.submit.data:

        post.title = form.post_title.data
        post.body = form.post_body.data
        post.last_edit = datetime.utcnow()
        post.category = form.category.data
        db.session.commit()

        flash('Changes saved.')
        return redirect(url_for('manage_blog'))

    elif request.method == 'GET':
        form.post_title.data = post.title
        form.post_body.data = post.body
        form.category.data = post.category

    return render_template('edit_blog_post.html', form=form, post=post)


# delete blog post
@app.route('/admin/delete_post/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    form = DeletePostForm()
    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()
    comments = BlogComment.query.filter_by(post_id=int(post_id)).all()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.delete(comments)
        db.session.commit()

        flash('Post deleted successfully.')
        return redirect(url_for('manage_blog'))

    return render_template('delete_post.html', form=form, post=post)


# manage (delete) blog comments
@app.route('/admin/manage_comments/<post_id>', methods=['GET', 'POST'])
@login_required
def manage_comments(post_id):

    post = BlogPost.query.filter_by(id=int(post_id)).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = (BlogComment.query.filter_by(post_id=int(post_id)).order_by(
                BlogComment.timestamp.desc()).paginate(
                page, app.config['COMMENTS_PER_PAGE'], False))

    next_url = url_for('manage_comments', post_id=post_id,
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('manage_comments', post_id=post_id,
                       page=comments.prev_num) \
        if comments.has_prev else None

    return render_template('manage_comments.html', post=post,
                           comments=comments.items, next_url=next_url,
                           prev_url=prev_url)


# delete comment and redirect back to manage comments
@app.route('/admin/delete_comment/<post_id>/<comment_id>',
           methods=['GET'])
@login_required
def delete_comment(comment_id, post_id):

    comment = BlogComment.query.filter_by(id=int(comment_id)).first_or_404()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('manage_comments', post_id=post_id))


# manage blog post categories
@app.route('/admin/edit_categories', methods=['GET', 'POST'])
@login_required
def edit_categories():

    add_cat = AddCategoryForm()
    categories = BlogCategory.query.all()

    # add new category
    if add_cat.validate_on_submit() and add_cat.submit.data:

        new_cat = BlogCategory(category=add_cat.category.data.lower())

        db.session.add(new_cat)
        db.session.commit()

        flash('Category added.')
        return redirect(url_for('edit_categories'))

    return render_template('edit_categories.html', add_cat=add_cat,
                           categories=categories)


# delete category and redirect back to edit category
@app.route('/admin/delete_category/<cat_id>',
           methods=['GET', 'POST'])
@login_required
def delete_category(cat_id):

    category = BlogCategory.query.filter_by(id=int(cat_id)).first_or_404()

    db.session.delete(category)
    db.session.commit()

    flash('Category removed.')
    return redirect(url_for('edit_categories'))
