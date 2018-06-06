from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import HiddenField
from wtforms.validators import DataRequired, Length, Email


# admin login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
    # SKIPPAR REMEMBER ME Så jag vet


# Blog post
class BlogPostForm(FlaskForm):
    post_title = TextAreaField('Post title', validators=[
        DataRequired(), Length(min=1, max=100)])
    post_body = TextAreaField('Post body', validators=[
        DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')


# Comment post
class BlogCommentForm(FlaskForm):
    comment_author = TextAreaField('Your Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    comment_email = TextAreaField('Your email', validators=[Email()])
    comment_body = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')
    post_id = HiddenField('', validators=[DataRequired()])
    # captcha ???
