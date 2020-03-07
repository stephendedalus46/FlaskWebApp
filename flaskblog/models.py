from datetime import datetime
from flaskblog import db, login_manager  # variables from init
from flask import current_app  # previously: from flaskblog import app  # to enable password change
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # to enable password change
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # line that set relationship with POST table(model)!! backref is like adding another column to the Post model,
                                                                  # lazy allow to get all posts from specific author
                                                                  # uppercase Post, becasuse of referencing to model name, not tablename

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{}','{}','{}')".format(self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # without brackets!!! we want to pass the function, not current time
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # lowercase user, because we reference tablename, not model name

    def __repr__(self):
        return "Post('{}','{}')".format(self.title, self.date_posted)