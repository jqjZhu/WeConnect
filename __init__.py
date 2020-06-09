from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

socketio = SocketIO(app)

db_name = 'projectDB'
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

############LOGIN CONFIGS##########################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

##################################################

from core.views import core
from users.views import users
from blog_posts.views import blog_posts
from error_pages.handlers import error_pages
from chats.views import chats

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)
app.register_blueprint(chats)