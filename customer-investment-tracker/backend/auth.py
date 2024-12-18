from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint for auth
auth = Blueprint('auth', __name__)

# Sample user database (replace with your database logic later)
users = [
    {"username": "admin", "password": generate_password_hash("password123")}
]

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400
    
    # Find the user
    user = next((u for u in users if u["username"] == data["username"]), None)
    
    if user and check_password_hash(user["password"], data["password"]):
        # Generate JWT token
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401

