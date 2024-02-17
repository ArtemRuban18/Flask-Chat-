from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators  import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),Length(min=5, max=20)])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField("Confirm", validators=[DataRequired(), EqualTo("password")])
    signup = SubmitField("SignUp")

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    signin = SubmitField("SignIn")

class CreateRoom(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    code = IntegerField("Code", validators=[DataRequired()])
    create_room = SubmitField("Create Room")
    join_room = SubmitField("Join Room")

class JoinRoom(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    code = IntegerField("Code", validators=[DataRequired()])
    join_room = SubmitField("Join Room")
    create_room = SubmitField("Create Room")
