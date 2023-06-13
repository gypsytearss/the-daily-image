from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    print(f"Current user: {current_user}")
    return render_template("index.html", current_user=True if current_user.is_authenticated else False)

@main.route("/profile")
@login_required
def profile():
    print(f"Current user {current_user}")
    return render_template("profile.html", name=current_user.name, current_user=True if current_user.is_authenticated else False)
