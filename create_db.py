from cw_app import db, app
from cw_app.models import User

with app.app_context():
    db.create_all()
