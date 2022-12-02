import os
from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import Project as Project, User as User, Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MPTEAM23'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user = session['user'])
    return render_template('index.html')

@app.route('/projects')
def get_projects():
    allprojects = db.session.query(Project).all()
    if session.get('user'):
        projects = db.session.query(Project).filter_by(manager=session['user_username']).all()
        return render_template('project/projects.html', projects = projects, allprojects = allprojects ,user=session['user'], username=session['user_username'] )
    else:
        return render_template('project/projects.html', allprojects = allprojects)

@app.route('/projects/<project_id>')
def get_project(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    if session.get('user'):
        form = CommentForm()
        return render_template('project/project.html', project = project, user=session['user'], username=session['user_username'], form=form)
    else:
        return render_template('project/project.html', project = project)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    
    if session.get('user'):
        if request.method == 'POST':
            
            title = request.form['title']
            text = request.form['projectText']
            from datetime import date
            today = date.today()
            today=today.strftime("%m-%d-%Y")
            placeholderImage = "https://s3-alpha.figma.com/hub/file/948140848/1f4d8ea7-e9d9-48b7-b70c-819482fb10fb-cover.png"
            new_record = Project(title, text, today, session['user_username'], placeholderImage)
            db.session.add(new_record)
            db.session.commit()
        
            return redirect(url_for('get_projects'))
        else:
            return render_template('project/new.html', user=session['user'])
    else:
        return redirect(url_for('login'))
    
@app.route('/projects/edit/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    if session.get('user'):
        if request.method == 'POST':
            
            title = request.form['title']
            text = request.form['projectText']
            image = request.form['projectImg']
            
            #find project by id, and make sure the user deleting the project is the project manager
            project = db.session.query(Project).filter_by(id=project_id, manager=session['user_username']).one()
            
            project.title = title
            project.text = text
            project.imageURL = image
            
            db.session.add(project)
            db.session.commit()
            
            return redirect(url_for('get_projects'))    
        else:
            my_project = db.session.query(Project).filter_by(id=project_id).one()
        
            return render_template('project/new.html', project=my_project, user=session['user'])
    else:
        return redirect(url_for('login'))
    
@app.route('/projects/<project_id>/comment', methods=['POST'])
def new_comment(project_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(project_id), session['user_username'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_project', project_id=project_id))

    else:
        return redirect(url_for('login'))

@app.route('/projects/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    
    if session.get('user'):
        #find project by id, and make sure the user deleting the project is the project manager
        project = db.session.query(Project).filter_by(id=project_id, manager=session['user_username']).one()
        
        db.session.delete(project)
        db.session.commit()
    
        return redirect(url_for('get_projects'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():

        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())

        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']

        new_user = User(first_name, last_name, username, request.form['email'], h_password)

        db.session.add(new_user)
        db.session.commit()

        session['user'] = first_name
        session['user_lname'] = last_name
        session['user_id'] = new_user.id 
        session['user_username'] = username
        session['user_email'] = new_user.email

        return redirect(url_for('get_projects'))

    # something went wrong - display register view
    return render_template('account/register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():

        the_user = db.session.query(User).filter_by(email=request.form['email']).one()

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):

            #Set session user, user id, username and email
            session['user'] = the_user.fname
            session['user_lname'] = the_user.lname
            session['user_id'] = the_user.id
            session['user_username'] = the_user.username
            session['user_email'] = the_user.email
 
            return redirect(url_for('get_projects'))

        login_form.password.errors = ["Incorrect username or password."]
        return render_template("account/login.html", form=login_form)
    else:
        return render_template("account/login.html", form=login_form)
    
@app.route('/account') 
def account():
    if session.get('user'): 
        projects = db.session.query(Project).filter_by(manager=session['user_username']).all()
        return render_template('account/account.html', user = session['user'], lname = session['user_lname'], projects = projects, username = session['user_username'], email = session['user_email'])
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)