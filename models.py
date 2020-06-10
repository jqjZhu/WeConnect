from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from __init__ import login_manager, db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable = False, default = 'default_profile.png')
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref = 'author', lazy = True)
    chats = db.relationship('ChatHistory', backref = 'author', lazy = True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"

class ChatHistory(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) #sender_id

    create_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # content = db.Column(db.Text, nullable = False)
    # receiver_id = db.Column(db.String(140), nullable = False)
    # read = db.Column(db.Boolean)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

def connect_to_db(app, db_name):

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app 

    connect_to_db(app, 'projectDB')
    print('Connected successfully')

    