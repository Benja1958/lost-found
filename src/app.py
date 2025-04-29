import datetime
from db import db
from flask import Flask, request, jsonify
from db import db, User, FoundItem
from datetime import datetime

import json

app = Flask(__name__)
db_filename = "lost_and_found.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(body, code=200):
    return jsonify(body), code

def failure_response(message, code=404):
    return jsonify({"error": message}), code

@app.route("/api/item/<int:item_id>/", methods=["GET"])
def get_item_by_ID(item_id):
    """
    Get an item by it's ID in the database
    """
    item = FoundItem.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("There's no item by that ID", 404)
    return success_response(item.serialize(), 200)

@app.route("/api/items/", methods=["GET"])
def get_all_lost_items():
    """
    Get all lost items
    """
    return success_response({ "items": [item.serialize() for item in FoundItem.query.all()] })

@app.route("/api/add_item/", methods=["POST"])
def add_new_lost_item():
    """
    Add a new item into the database
    """
    body = request.get_json(force=True)

    name = body.get("name", None)
    email = body.get("email", None)
    phone_number = body.get("phone_number", None)

    title = body.get("title", None)
    description = body.get("description", None)
    location_found = body.get("location_found", None)
    date_found = body.get("date_found", None)
    image = body.get("image", None)

    if name is None or email is None or phone_number is None:
        return failure_response("name, email, or phone number fields should not be empty", 400)
    if title is None:
        return failure_response("title field should not be empty", 400)
    if description is None:
        failure_response("description field should not be empty", 400)
    if location_found is None:
        failure_response("location field should not be empty", 400)
    if date_found is None:
        failure_response("date_found field should not be empty", 400)

    user = get_or_create_user(name, email, phone_number)

    new_item = FoundItem(
        description=description,
        location=location_found,
        date_found=datetime.fromisoformat(date_found),
        image_url=image,
        user_id=user.id
    )

    db.session.add(new_item)
    db.session.commit()
    return success_response(new_item.serialize(), 201)

@app.route("/api/users/", methods=["POST"])
def get_or_create_user_route():
    """
    Create a new user, or get the existing one if they already exist.
    """
    body = request.get_json(force=True)

    name = body.get("name")
    email = body.get("email")
    phone_number = body.get("phone_number")

    if not all([name, email, phone_number]):
        return failure_response("name, email, and phone_number are required", 400)

    user = get_or_create_user(name, email, phone_number)

    return success_response(user.serialize(), 200)


def get_or_create_user(name, email, phone_number):
    """
    Get a user by email, or create a new one if not found.
    """
    user = User.query.filter_by(email=email).first()
    if user:
        return user

    # Create new user
    new_user = User(username=name, email=email, phone=phone_number)
    db.session.add(new_user)
    db.session.commit()
    return new_user

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
