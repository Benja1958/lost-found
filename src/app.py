from db import db
from flask import Flask, request, jsonify
from db import db, User, FoundItem

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
    pass

@app.route("/api/items/", methods=["GET"])
def get_all_lost_items():
    """
    Get all lost items
    """
    pass

@app.route("/api/add/", methods=["POST"])
def add_new_lost_item():
    """
    Add a new item into the database
    """
    pass