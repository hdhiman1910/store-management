from flask import Blueprint, request, jsonify
from flask_security import verify_password, hash_password
from models import User, db
from flask import current_app

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

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

@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']

    active = True


    if (not name) or (not email) or (not password):
        return jsonify({"message":"all three fields are required!"})

    if role == "manager":
        active = False

    datastore = current_app.datastore

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "user already exist"}), 400

    datastore.create_user(name=name, email=email, password=hash_password(password), active=active)
    db.session.commit()

    role=datastore.find_role(role)
    user = datastore.find_user(email=email)
    datastore.add_role_to_user(user, role)

    datastore.add_role_to_user(user, role)
    db.session.commit()

    return jsonify({
        "id" : user.id,
        "email": user.email,
        "name": user.name
    }), 201