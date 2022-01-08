import os
import secrets
from PIL import Image
from include import app, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from include.forms import Register, Login, UpdateAccount, UpdatePassword, NewPost
from include.models import User, Post
from include import db, login_manager
from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.all()
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
    pswd_form = UpdatePassword()
    update_form.username.data = current_user.username
    update_form.email.data = current_user.email

    if update_form.submit1.data and update_form.validate():
        initial_pic = current_user.image_file
        if update_form.picture.data:
            current_user.image_file = save_picture(update_form.picture.data)
        initial_email = current_user.email
        initial_username = current_user.username
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        if initial_pic != current_user.image_file:
            flash('Profie pic updated!', category='success')
        if initial_username != update_form.username.data or initial_email != update_form.email.data:
            flash('Account credentials updated successfully!', category='success')
        else:
            flash('Account credentials unchanged.', category='primary')
        return redirect(url_for('account'))
    
    if pswd_form.submit2.data and pswd_form.validate():
        current_user.password_hash = bcrypt.generate_password_hash(pswd_form.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Password updated!', category='success')
        return redirect(url_for('account'))

    if pswd_form.errors != {}:
        for category, err_msgs in pswd_form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error updating account: {err_msg}', category='danger')

    if update_form.errors != {}:
        for category, err_msgs in update_form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error updating account: {err_msg}', category='danger')

    img_file = url_for('static', filename='profilepics/' + current_user.image_file)
    return render_template('account.html', img_file=img_file, update_form=update_form, pswd_form=pswd_form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data,  content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Post uploaded successfully!', category='success')
        return redirect(url_for('index'))
    return render_template('post.html', form=form, Legend='New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('get_post.html', post=post)


@app.route('/post/<int:post_id>/update')
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPost()
    return render_template('post.html', form=form, post=post, Legend='Update Post')


def save_picture(profile_pic):
    os.remove(app.root_path + '\static\profilepics\\' + current_user.image_file)
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(profile_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path + '\static\profilepics\\' + picture_fn) 
    img = Image.open(profile_pic)
    img.thumbnail((125, 125))
    img.save(picture_path)
    return picture_fn