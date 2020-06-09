from models import db
from __init__ import socketio, app
#question: why do I still need to import socketio here as socketio has been imported from project
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from datetime import datetime
from time import strftime, localtime

chats = Blueprint('chats', __name__)
MESSAGES = ["message1", "message2"]

@chats.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', username=current_user.username, messages=MESSAGES)

@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")

    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%P', localtime())}, messages=data['message'])

@socketio.on('join')
def join(data):

    join_room(data['message'])


@socketio.on('leave')
def leave(data):
     leave_room(data['message'])
