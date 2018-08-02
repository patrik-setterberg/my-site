from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# help Flask-Login talk to database (get id for user)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# ## Homepage ## #
class HomePageContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text_body = db.Column(db.String(5000))

    def __repr__(self):
        return '<Presentation {}>'.format(self.title)


# ## Portfolio ## #
class PortfProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(3000))
    url = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    cover_img_filename = db.Column(db.String(140), default=None)
    cover_img_alt_txt = db.Column(db.String(100), default=None)
    link_text = db.Column(db.String(50), default="Link to page")

    def __repr__(self):
        return '<Project {}>'.format(self.name)


# ## Blog ## #
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('BlogComment', backref='blog_post',
                               lazy='dynamic')
    last_edit = db.Column(db.DateTime, index=True)
    category = db.Column(db.String(32))
    photo_filename = db.Column(db.String(100), nullable=True)
    photo_alt_text = db.Column(db.String(140), default="Image alt text")
    post_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class BlogComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    email = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<comment {}>'.format(self.body)


class BlogCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(32))

    def __repr__(self):
        return '<cat {}>'.format(self.category)
