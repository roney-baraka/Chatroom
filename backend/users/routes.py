from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint('users',__name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Handling of registration logic 
        return redirect(url_for(users_bp.login))
    return render_template('register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Login logic 
        return redirect(url_for('users.dashboard'))
    return render_template('login.html')

