from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from __init__ import login_manager, db
from flask import session, request

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable = False, default = 'default_profile.png')
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref = 'author', lazy = True)
    # chats = db.relationship('ChatHistory', backref = 'author', lazy = True)
    comments = db.relationship('BlogComment', backref = 'user_comment', lazy = True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):

    __tablename__ = 'blog_post'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)

    comments = db.relationship('BlogComment', backref = 'post_comment', lazy = True)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"


# class ChatHistory(db.Model):
#     __tablename__ = 'chathistory'

#     id = db.Column(db.Integer, primary_key = True)
#     user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) 
#     user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) 

#     date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     content = db.Column(db.Text, nullable = False)
#     read = db.Column(db.Boolean)

#     def __init__(self, user1_id, user2_id, content):
#         self.content = content
#         self.user1_id = user1_id
#         self.user2_id = user2_id

#     def __repr__(self):
#         return f"user1_id: {self.user1_id} -- user2_id: {self.user2_id} -- Date: {self.date} --- {self.content}"

# class Chats(db.Model):
#     __tablename__ = 'chat'

#     id = db.Column(db.Integer, primary_key = True)
#     user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) 
#     user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) 


#     def __init__(self, content, user_id):
#         self.content = content
#         self.user_id = user_id


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key = True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    comment = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, comment, user_id, blog_post_id):
        self.comment = comment
        self.user_id = user_id
        self.blog_post_id = blog_post_id

    def __repr__(self):
        return f"Comment ID: {self.id} -- Date: {self.date}"


def connect_to_db(app, db_name):

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app 

    connect_to_db(app, 'projectDB')
    print('Connected successfully')

    