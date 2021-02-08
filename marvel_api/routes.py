from marvel_api import app, db
from flask import render_template, request, redirect, url_for, flash, session

from marvel_api.forms import UserLoginForm
from marvel_api.models import User, check_password_hash

#imports for flask login
from flask_login import login_user, logout_user, current_user, login_required


import os
# from marvel_api.helpers import get_jwt, token_required, verify_owner

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('signin'))
    except:
        raise Exception('Invalid For Data: Please Check your form')

    return render_template('signup.html', form=form)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('home'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('signin'))
    except:
        raise Exception('Invalid For Data: Please Check your form')

    return render_template('signin.html', form=form)
