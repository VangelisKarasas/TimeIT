from FlaskTimeIT import db
from datetime import datetime
from FlaskTimeIT import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    customer = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.String(15), nullable=False)
    minutes = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.description}','{self.date_created}','{self.customer}')"


class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=True)
    stop_time = db.Column(db.DateTime, nullable=True)
    # Store total duration in seconds
    total_duration = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def start(self):
        self.start_time = datetime.utcnow()
        self.stop_time = None

    def stop(self):
        if self.start_time:
            self.stop_time = datetime.utcnow()
            elapsed = (self.stop_time - self.start_time).total_seconds()
            self.total_duration += elapsed
            self.start_time = None  # Reset the start time

    def reset(self):
        self.start_time = None
        self.stop_time = None
        self.total_duration = 0.0
