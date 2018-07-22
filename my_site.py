from app import app, db
from app.models import User, BlogPost, BlogComment


# configures shell context (for 'flask shell'):
# pre-imports the application instance, app
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'BlogPost': BlogPost,
            'BlogComment': BlogComment}


# count comments for provided blog post
def count_comments(post_id):
    comments = BlogComment.query.filter_by(post_id=post_id)
    comment_count = comments.count()
    return comment_count


app.jinja_env.globals.update(count_comments=count_comments)
