from app import create_app, db, cli
from app.models import User, Artist, Album

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Artist=Artist, Album=Album)