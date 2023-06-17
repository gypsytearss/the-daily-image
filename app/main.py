from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import db
from .models import Images

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", current_user=current_user)

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, current_user=current_user)

@main.route("/image")
def new_image():

    image = Images.query.first()
    print("Image url {image.url}")

    return render_template("image.html",
                           current_user=current_user,
                           image_url=image.url,
                           title=image.title,
                           artist=image.creator)