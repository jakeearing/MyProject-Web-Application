import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Project as Project
#from models import Task as Task
#from models import User as User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    my_projects = db.session.query(Project).all()
    return render_template('project/projects.html', projects=my_projects)

@app.route('/project/<project_id>')
def project():
    return render_template('project/project.html')

@app.route('/projects/new', methods=['GET', 'POST'])
def new_note():
    print('request method is',request.method)
    return render_template('new.html')

@app.route('/notes/edit/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    
        return render_template('new.html')

@app.route('/notes/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    
    return redirect(url_for('get_projects'))


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)