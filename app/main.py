import sqlalchemy
import uuid

from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy.sql.expression import cast

from . import db
from .models import Images, UserImages

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", current_user=current_user)

@main.route("/profile")
@login_required
def profile():
    user_images = db.session.query(
        UserImages, Images, UserImages
        ).filter(cast(Images.uuid, sqlalchemy.String) == cast(UserImages.image_uuid, sqlalchemy.String)
                 ).order_by(UserImages.timestamp.asc()).all()
    return render_template("profile.html", current_user=current_user, user_images=user_images)

@main.route("/image", methods=["GET"])
def new_image():

    # TODO: implement logic for selecting randomly without overlap of existing user images
    # if current_user.is_authenticated:
    #     image = db.session.query(
    #         Images, UserImages
    #                 ).filter(UserImages.user_id == current_user.id
    #                 ).filter(
    #                 )
    image = Images.query.first()

    return redirect(url_for("main.image", image_uuid=image.uuid))


@main.route("/image/<image_uuid>", )
def image(image_uuid=None):

    res = db.session.query(Images)
    image = res.filter(cast(Images.uuid, sqlalchemy.String) == image_uuid).first()

    return render_template("image.html",
                           current_user=current_user,
                           image=image,
        )

@main.route("/image/<image_uuid>", methods=["POST"])
@login_required
def save_image(image_uuid=None):

    image_uuid = uuid.UUID(image_uuid)
    annotation = request.form.get("newDescription")

    user_image = UserImages(
        user_id=current_user.id,
        image_uuid=image_uuid,
        timestamp=sqlalchemy.sql.func.now(),
        annotation=annotation,
    )

    db.session.merge(user_image)
    db.session.commit()

    flash('Image description saved.')
    return redirect(url_for('main.image', image_uuid=image_uuid))


