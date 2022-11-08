from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Team23_App.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context