from flask import render_template, url_for, flash, redirect
from FlaskTimeIT import app, db, bcrypt
from FlaskTimeIT.forms import RegistrationForm, LoginForm
from FlaskTimeIT.models import User, Post
from flask_login import login_user, current_user


posts = [
    {
        'author': 'Corey Stapher',
        'title': 'Blog 1',
        'content': 'First Post Content',
        'date_posted': 'April 21,2018',
        'content': 'True'
    },
    {
        'author': 'Corey Stapher',
        'title': 'Blog 1',
        'content': 'First Post Content',
        'date_posted': 'April 21,2018',
        'content': 'True'
    }
]


@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def About():
    return render_template('About.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account created for {form.username.data}! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('Home'))
        else:
            flash('Login failed. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
