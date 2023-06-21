import random
import sqlalchemy
import uuid

from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import cast
from typing import Optional

from . import db
from .models import Images, UserImages

main = Blueprint("main", __name__)

@main.route("/")
def index():
    """
    Route for base splash page.
    """
    return render_template("index.html", current_user=current_user)

@main.route("/profile")
@login_required
def profile():
    """
    Route to view profile of annotated images for this user.
    """
    user_images = db.session.query(UserImages.user_id, UserImages.timestamp, UserImages.image_uuid, UserImages.annotation, Images.thumbnail_url
                    ).filter(Images.uuid == UserImages.image_uuid
                    ).filter(UserImages.user_id == current_user.id
                    ).order_by(UserImages.timestamp.asc()
                    ).all()
    return render_template("profile.html", current_user=current_user, user_images=user_images)

@main.route("/image", methods=["GET"])
def new_image():
    """
    Route to fetch a random new image to caption.
    
    Note: For authenticated users, this will not overlap with images they've already annotated.
    """
    all_images = {y[0] for y in db.session.query(Images.uuid).all()}
    
    if current_user.is_authenticated:
        completed_images = {x[0] for x in db.session.query(UserImages.image_uuid).filter(UserImages.user_id == current_user.id).all()}

        image_uuid = random.sample(all_images.difference(completed_images), 1)[0]
    else:
        image_uuid = random.sample(all_images, 1)[0]

    return redirect(url_for("main.image", image_uuid=image_uuid))


@main.route("/image/<image_uuid>", )
def image(image_uuid: str = None):
    """
    Route to present a selected image for annotation / updating.
    """

    res = db.session.query(Images)
    image_uuid = uuid.UUID(image_uuid).hex

    image = res.filter(cast(Images.uuid, sqlalchemy.String) == image_uuid).first()

    
    # If current user is logged in, include current caption in presentation
    annotation: Optional[str] = None
    if current_user.is_authenticated:
        user_image = db.session.query(UserImages
                                      ).filter(cast(UserImages.image_uuid, sqlalchemy.String) == image_uuid
                                      ).filter(UserImages.user_id == current_user.id
                                      ).first()
        if user_image:
            annotation = user_image.annotation

    return render_template("image.html",
                           current_user=current_user,
                           image=image,
                           annotation=annotation,
        )

@main.route("/image/<image_uuid>", methods=["POST"])
@login_required
def save_image(image_uuid=None):
    """
    Route to post a new / updated annotation to the database.
    """

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


