from app import app, db
from app.models import User, BlogPost, BlogComment


# Configures shell context (for 'flask shell'):
# pre-imports the application instance, app
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'BlogPost': BlogPost,
            'BlogComment': BlogComment}


# Count posts in a category
def count_posts(category):
    posts = BlogPost.query.filter_by(category=category)
    post_count = posts.count()
    return post_count


# Count comments for provided blog post
def count_comments(post_id):
    comments = BlogComment.query.filter_by(post_id=post_id)
    comment_count = comments.count()
    return comment_count


# add leading zeros to post id
def format_id(post_id):
    formatted = "{:03}".format(post_id)
    return formatted


app.jinja_env.globals.update(count_comments=count_comments,
                             count_posts=count_posts, format_id=format_id)
