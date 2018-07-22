from app import images
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import TextField, HiddenField, SelectField
from wtforms import ValidationError
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
    category = SelectField('Category')
    photo = FileField('Post photo', validators=[
                      FileAllowed(images, 'Only images allowed.')])
    photo_alt_text = TextField('Photo alt-text')
    submit = SubmitField('Submit post')


# Add new blog tags
class AddCategoryForm(FlaskForm):
    category = TextField('Add category', validators=[DataRequired()])
    submit = SubmitField('Add Category')


# Comment post
class BlogCommentForm(FlaskForm):
    comment_author = TextField('Your Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    comment_email = TextField('Your email', validators=[Email()])
    comment_body = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=1, max=1000)])
    recaptcha = RecaptchaField()
    post_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Delete blog post
class DeletePostForm(FlaskForm):
    del_field = TextField("Input 'DELETE' to delete post", validators=[
                          InputRequired(), Length(min=1, max=10)])
    submit = SubmitField('Delete Post')

    def validate_del_field(FlaskForm, field):
        if field.data != 'DELETE':
            raise ValidationError('Please confirm deletion. Properly.')


# Edit blog post score
class EditScoreForm(FlaskForm):
    score = TextField('', validators=[DataRequired(),
                      Length(min=1, max=5)])
    submit = SubmitField('Update score')
