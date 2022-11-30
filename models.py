from database import db
import datetime

class Project(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    manager = db.Column(db.String, db.ForeignKey("user.fname"), nullable=False)
    imageURL = db.Column("imageURL", db.String, nullable=True)
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)

    def __init__(self, title, text, date, manager):
        self.title = title
        self.text = text
        self.date = date
        self.manager = manager

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column("fname", db.String(50))
    lname = db.Column("lname", db.String(50))
    username = db.Column("username", db.String(50))
    email = db.Column("email", db.String(50))
    password = db.Column("password", db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    projects = db.relationship("Project", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __init__(self, fname, lname, username, email, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    user_name = db.Column(db.Integer, db.ForeignKey("user.fname"), nullable=False)

    def __init__(self, content, project_id, user_name):
        self.date_posted = datetime.date.today()
        self.content = content
        self.project_id = project_id
        self.user_name = user_name