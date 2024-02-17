from app import socketio
from flask_socketio import emit
import random
from flask import session
from datetime import datetime
import os

def generate_random_color():
     red = random.randint(0, 255)
     green = random.randint(0, 255)
     blue = random.randint(0, 255)

     return f"rgb({red}, {green}, {blue})"

def logFileForRooms(room_id,room_name, sender_name,content):
    logDirectory = r"C:\Users\User\OneDrive\Рабочий стол\Flask Chat\app\log_files"
    senderNameStr = str(sender_name)
    sanitizedSenderName = senderNameStr.replace('<', '_').replace('>', '_')
    logFileName = f"log_{room_name}_{sanitizedSenderName}.txt"

    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)
    
    with open(os.path.join(logDirectory,logFileName ),'a') as logFile:
         logFile.write(f"[{datetime.utcnow().strftime('%H:%M:%S')}]: Sender:{sender_name}: {content}\n")
         logFile.close()


@socketio.on('connect')
def connect(data):
    if 'color' not in session:
        session['color'] = generate_random_color()
    username = session.get('username', 'name')
    emit('color_update', {'color': session['color']})
    emit('message', {'name': username, 'message': 'User connected'}, broadcast=True)
    print("Connect")

@socketio.on('disconnect')
def disconnect():
    username = session.get('username', 'name')
    emit('message',{'name': username, 'message':'User disconnected'}, broadcast=True)
    print("Disconnect")

@socketio.on('message')
def handle_message(data):
    room_id = data.get('room_id')
    sender_name = data.get('name')
    content = data.get('message')
    current_room_name = session.get('current_room_name')
    logFileForRooms(room_id, current_room_name, sender_name, content)

    print("Message: " + data['message'])
    color = generate_random_color()
    emit('message', {'name': data['name'], 'message': data['message'], 'color': color}, broadcast=True)

