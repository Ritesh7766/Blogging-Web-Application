from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from include import db, bcrypt
from include.models import User, Post
from include.users.forms import Register, Login, UpdateAccount, UpdatePassword, RequestResetForm, ResetPasswordForm
from include.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email = form.email.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash(f'Incorrect username or password', category='danger')
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}!', category = 'success')
        return redirect(url_for('users.login'))
    if form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='success')
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    
    if pswd_form.submit2.data and pswd_form.validate():
        current_user.password_hash = bcrypt.generate_password_hash(pswd_form.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Password updated!', category='success')
        return redirect(url_for('users.account'))

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


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect('index')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('User with this email doesnot exists!', category='warning')
            return redirect(url_for('users.reset_request'))
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', category='primary')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect('main.index')
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token!', categoy='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()
        flash(f'Password reset successful!', category = 'success')
        return redirect(url_for('users.login'))
    if form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'Error resetting password.', category='danger')
    return render_template('reset_password.html', form=form)