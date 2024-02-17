from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .models import Users, ChatRoom
from .forms import RegisterForm, LoginForm, CreateRoom,JoinRoom
from datetime import datetime
import os
from .events import logFileForRooms

@login_manager.user_loader
def load_user(id):
      return db.session.query(Users).get(int(id))


@app.route('/')
def index():
      return render_template('index.html')


@app.route('/create', methods = ['GET','POST'])
@login_required
def create():
    form = CreateRoom()
    rooms = ChatRoom.query.all()
    users = Users.query.all()
    if form.validate_on_submit():
        room_name = form.name.data
        room_code = form.code.data
        room = ChatRoom.query.filter_by(name = form.name.data).first()
        code_room = ChatRoom.query.filter_by(code = room_code).first()
        if room:
            flash("Room is exists! Try other name", 'warning')
            return redirect(url_for('create'))
        if code_room:
            flash("Code is already in use!", 'warning')
            return redirect(url_for('create'))
        if not room:
            new_room = ChatRoom(name = room_name, code = room_code)
            db.session.add(new_room)
            db.session.commit()
            session['current_room_name'] = room_name  # Set current room name in session
            logFileForRooms(new_room.id, new_room.name, current_user.name, "Log file created")
            return redirect(url_for('room', room_id=new_room.id, room_name=new_room.name))
    return render_template("create.html", form=form, rooms=rooms, users=users, current_user=current_user)



@app.route("/join", methods = ['GET','POST'])
@login_required
def join():
    form = JoinRoom()
    rooms = ChatRoom.query.all()
    if form.validate_on_submit():
        room_name = form.name.data
        room_code = form.code.data
        room = ChatRoom.query.filter_by(name = room_name).first()
        if room and room.code == room_code:
            return redirect(url_for('room'))
        else:
            flash("This room is not creat!")
            return redirect(url_for('join'))
    return render_template('join.html',form = form, rooms = rooms)


@app.route('/room', methods = ['GET','POST'])
@login_required
def room():
    username = session.get('username')
    if username:
         return render_template("room.html", username=username)
    else:
         return redirect(url_for('signin'))


@app.route('/signup', methods = ['GET', 'POST'])
def SignUp():
      form = RegisterForm()
      if form.validate_on_submit():
            userIsRegistered = Users.query.filter_by(name = form.name.data).first()
            if userIsRegistered:
                  flash("User with this name is registered!")
                  return redirect(url_for('signin'))
            password_hash = generate_password_hash(password= form.confirm_password.data)
            new_user = Users(name = form.name.data, password = password_hash)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signin'))
      return render_template('signup.html', form = form)


@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name = form.name.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = user.name
            return redirect(url_for('join'))
    return render_template('signin.html', form=form)
     
               
@app.route('/logout')
@login_required
def logout():
     logout_user()
     session.pop('username')
     return render_template('index.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_room(id):
    room = ChatRoom.query.get(id)
    if room:
        db.session.delete(room)
        db.session.commit()
    return redirect(url_for('create'))


