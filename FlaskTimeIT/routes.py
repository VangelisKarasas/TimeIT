from flask import render_template, url_for, flash, redirect, request
from FlaskTimeIT import app, db, bcrypt
from FlaskTimeIT.forms import RegistrationForm, LoginForm, PostForm
from FlaskTimeIT.models import User, Post, Timer
from flask import jsonify
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'Description': 'POS Update',
        'Customer': 'Candia',
        'Debit Hours': '1',
        'date_created': 'April 25,2018',
        'User': 'vag'
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        else:
            flash('Login failed. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('Home'))


@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename=current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(description=form.description.data,
                    customer=form.customer.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created', 'success')
        return redirect(url_for('Home'))

    return render_template('create_post.html', title='New Post', form=form)


@app.route('/timer/start', methods=['GET', 'POST'])
@login_required
def start_timer():
    # Check if a timer exists for this user
    timer = Timer.query.filter_by(user_id=current_user.id).first()
    if not timer:
        timer = Timer(user_id=current_user.id)

    # Start the timer
    timer.start()
    db.session.add(timer)
    db.session.commit()

    flash('Timer started!', 'success')
    return redirect(url_for('Home'))


@app.route('/timer/stop', methods=['POST'])
@login_required
def stop_timer():
    # Get the user's timer
    timer = Timer.query.filter_by(user_id=current_user.id).first()

    if timer and timer.start_time:
        # Stop the timer
        timer.stop()
        db.session.commit()
        flash('Timer stopped!', 'success')
    else:
        flash('No active timer found.', 'warning')

    return redirect(url_for('Home'))


@app.route('/timer/status')
@login_required
def timer_status():
    # Get the user's timer
    timer = Timer.query.filter_by(user_id=current_user.id).first()

    if timer:
        # Calculate current running time if the timer is active
        if timer.start_time:
            current_duration = (datetime.utcnow() -
                                timer.start_time).total_seconds()
        else:
            current_duration = 0

        return jsonify({
            'total_duration': timer.total_duration,
            'current_duration': current_duration
        })

    return jsonify({'error': 'No timer found for this user'}), 404
