"/login"

from flask import Blueprint, request, jsonify
from flask_security import verify_password
from models import User

auth_bp = Blueprint("auth", __name__,  url_prefix="/auth")

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    if (not email) or (not password):
        return jsonify({"message": "both email and password fields are required!"}), 400
    
    user = User.query.filter_by(email = email).first_or_404()


    if not verify_password(password, user.password):
        return jsonify({"message": "wrong password"}), 400
    return jsonify({"id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "token": user.get_auth_token()}), 200