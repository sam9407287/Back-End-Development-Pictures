from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return a picture by id"""
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    abort(404, description=f"Picture with id {id} not found")

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create picture"""
    new_picture = request.get_json()
    if not new_picture:
        abort(400, description="Invalid input: No data provided")

    for picture in data:
        if picture["id"] == new_picture["id"]:
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201
######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update an existing picture"""
    updated_picture = request.get_json()
    if not updated_picture:
        abort(400, description="Invalid input: No data provided")

    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = updated_picture
            return jsonify(updated_picture), 200

    abort(404, description=f"Picture with id {id} not found")

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture by id"""
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(i)
            return "", 204

    abort(404, description=f"Picture with id {id} not found")