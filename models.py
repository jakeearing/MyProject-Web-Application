from database import db

class Project(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    managerID = db.Column("managerID", db.Integer)
    
    def __init__(self, title, text, date, managerID):
        self.title = title
        self.text = text
        self.date = date
        self.managerID = managerID
        
class Tasks(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    
    def __init__(self, title, text, date, managerID):
        self.title = title
        self.text = text
        self.date = date
        self.managerID = managerID
        
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password