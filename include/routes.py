from include import app
from flask import render_template, url_for, flash, redirect
from include.forms import Register, Login
from include.models import User, Post
from include import db, login_manager
from flask_login import login_user

posts = [
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email = form.email.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('index'))
        else:
            flash(f'Incorrect username or password', category='danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}!', category = 'success')
        return redirect(url_for('login'))
    if form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)