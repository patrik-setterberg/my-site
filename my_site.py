from app import app, db
from app.models import User, BlogPost, BlogComment


# configures shell context (for 'flask shell'):
# pre-imports the application instance, app
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'BlogPost': BlogPost,
            'BlogComment': BlogComment}
