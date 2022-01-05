from include import app
from flask import render_template, url_for, flash, redirect
from include.forms import Register, Login

posts = [
]

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
        if form.email.data == 'rites@gmail.com' and form.password.data == '1234567890':
            flash('User logged in successfully', category='success')
        else:
            flash('Wrong credentials', category='warning')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('index'))
    if form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)