import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Project as Project
#from models import Task as Task
from models import User as User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    a_user =  db.session.query(User).filter_by(email='jearing@uncc.edu').one()
    return render_template('index.html', user=a_user)

@app.route('/projects')
def get_projects():
    a_user =  db.session.query(User).filter_by(email='jearing@uncc.edu').one()
    my_projects = db.session.query(Project).all()
    return render_template('project/projects.html', projects = my_projects, user = a_user)

@app.route('/projects/<project_id>')
def get_project(project_id):
    a_user =  db.session.query(User).filter_by(email='jearing@uncc.edu').one()
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    return render_template('project/project.html', project=my_project, user = a_user)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    
    print('request method is',request.method)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['projectText']
        from datetime import date
        today = date.today()
        today=today.strftime("%m-%d-%Y")
        
        new_project = Project(title, text, today)
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('get_projects'))
    else:
        a_user =  db.session.query(User).filter_by(email='jearing@uncc.edu').one()
        return render_template('project/new.html', user=a_user)
    
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    if request.method == 'POST':
        
        title = request.form['title']
        
        text = request.form['projectText']
        project = db.session.query(Project).filter_by(id=project_id).one()
        
        project.title = title
        project.text = text
        
        db.session.add(project)
        db.session.commit()
        
        return redirect(url_for('get_projects'))
    
    else:
        a_user = db.session.query(User).filter_by(email='jearing@uncc.edu').one()
    
        my_project = db.session.query(Project).filter_by(id=project_id).one()
    
        return render_template('new.html', project=my_project, user=a_user)

@app.route('/projects/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(my_project)
    db.session.commit()
    
    return redirect(url_for('get_projects'))
    

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)