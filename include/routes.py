from include import app
from flask import render_template, url_for, flash, redirect, request
from include.forms import Register, Login, UpdateAccount
from include.models import User, Post
from include import db, login_manager
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': '''First post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content''',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': '''Second post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentvFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content
        First post contentFirst post contentFirst post contentFirst post content''',
        'date_posted': 'April 21, 2018'
    }
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

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email = form.email.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_form = UpdateAccount()
    if update_form.validate_on_submit():
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        if current_user.username != update_form.username.data or current_user.email != update_form.email.data:
            flash('Your account has been updated successfully!', category='success')
        else:
            flash('No changes made to the account.', category='primary')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    if update_form.errors != {}:
        for category, err_msgs in update_form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error updating account: {err_msg}', category='danger')
    img_file = url_for('static', filename='profilepics/' + current_user.image_file)
    return render_template('account.html', img_file=img_file, update_form=update_form)