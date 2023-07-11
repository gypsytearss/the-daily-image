from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

user = Blueprint('user', __name__)


@user.route('/login')
def login():
    """
    GET the login page.
    """
    return render_template("login.html", current_user=current_user)


@user.route('/login', methods=['POST'])
def login_post():
    """
    POST input login data to the server to authenticate.
    """
    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    remember = True if request.form.get('flexCheckDefault') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(
            url_for('user.login')
        )    # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@user.route('/signup')
def signup():
    """
    GET the signup page.
    """
    return render_template("signup.html", current_user=current_user)


@user.route('/signup', methods=["POST"])
def signup_post():
    """
    POST sign up data to the server to add a new user.

    Note: Redirects to the sign up page with a warning message if user email already in use.
    """
    # code to validate and add user to database goes here
    email = request.form.get('inputEmail')
    name = request.form.get('inputName')
    password = request.form.get('inputPassword')

    user = User.query.filter_by(email=email).first(
    )    # if this returns a user, then the email already exists in database

    if user:    # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('user.login'))


@user.route('/logout')
@login_required
def logout():
    """
    GET logs user out of currently logged-in account.
    """
    logout_user()
    return redirect(url_for("main.index"))