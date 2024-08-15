from flask import Flask, render_template, redirect, url_for, request, flash
from flask_socketio import SocketIO, send
from flask_login import LoginManager, UserMixin, logout_user, logout_user, current_user, login_required
import os
from flask_login import login_user
from extensions import db
import secrets 
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate and set the secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password ):
        self.password_hash = password # hashing for real applications 

    def check_password(self, password ):
        return self.password_hash == password


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

@app.route('/')
@login_required
def index():
    return render_template('chat.html' , username=current_user.username)

@app.route('/login', methods =['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user is None:
            new_user = User(username=username, email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        else:
            flash('User with this username or email already exists')

    return render_template('register.html')


    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(login))

@socketio.on('connect')
def handle_connect(auth):
    if current_user.is_authenticated:
        print(f'{current_user.username} has connected')
        send(f'{current_user.username} has joined the chat', broadcast=True)
    else:
        print('An anonymous user has connected')


@socketio.on('message')
def handle_message(msg):
    print(f'{current_user.username}: {msg}')
    send(f'{current_user.username}: {msg}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)