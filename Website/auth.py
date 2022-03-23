from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#blueprint means it has a bunch of urls defined in here
#Helps us seperate and organize our views

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['Get', 'Post'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)
            else:
                flash("Incorrect password, try again", category='error')
        else:
            flash('Email does not exist', category='error')

    data = request.form
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['Get', 'Post'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get("firstName")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exits', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exits', category='error')
        elif len(email) < 4:
            flash('email invalid', category='error')
        elif len(firstName) < 2:
            flash('first name invalid', category='error')
        elif password1 != password2:
            flash('Passwords dont match! ', category='error')
        elif len(password1) < 2:
            flash('password is less than 7 characters', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='sucess')# Add them to database
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


# @auth.route('/admin/')
# def adminlog():
#     return redirect(url_for('auth.adminlog'))

