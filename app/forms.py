from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import TextField, HiddenField, ValidationError
from wtforms.validators import DataRequired, InputRequired, Length, Email


# Admin login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


# Blog post
class BlogPostForm(FlaskForm):
    post_title = TextField('Post title', validators=[
        DataRequired(), Length(min=1, max=100)])
    post_body = TextAreaField('Post body', validators=[
        DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')


# Comment post
class BlogCommentForm(FlaskForm):
    comment_author = TextField('Your Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    comment_email = TextField('Your email', validators=[Email()])
    comment_body = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=1, max=1000)])
    post_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
    # captcha ???


# Delete blog post
class DeletePostForm(FlaskForm):
    del_field = TextField("Input 'DELETE' to delete post", validators=[
                          InputRequired(), Length(min=1, max=10)])
    submit = SubmitField('Delete Post')

    def validate_del_field(FlaskForm, field):
        if field.data.lower() != 'delete':
            raise ValidationError('Please confirm deletion. Properly.')
