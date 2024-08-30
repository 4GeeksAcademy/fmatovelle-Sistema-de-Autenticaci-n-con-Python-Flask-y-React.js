from flask import Flask, request, jsonify, url_for, Blueprint, abort
from api.models import db, User, Person, Vehicle, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)  # Keep only one Blueprint instance

# Allow CORS requests to this API
CORS(api)

# Implement Signup Endpoint
@api.route('/signup', methods=['POST'])
def signup():
    # Get data from the request
    data = request.get_json()

    # Check if email and password are provided
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    # Check if the email already exists
    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)

    # Create a new User object
    new_user = User(email=data['email'], password=hashed_password, is_active=True)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a success message
    return jsonify({"message": "User created successfully"}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {current_user}!"}), 200

@api.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()  
    return jsonify([person.serialize() for person in people])  

@api.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    person = Person.query.get(people_id)  
    if person is None:
        abort(404) 
    return jsonify(person.serialize())  

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all() 
    return jsonify([planet.serialize() for planet in planets])  

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        abort(404)  
    return jsonify(planet.serialize())

@api.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all() 
    return jsonify([vehicle.serialize() for vehicle in vehicles])  

@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        abort(404)  
    return jsonify(vehicle.serialize())

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all() 
    return jsonify([user.serialize() for user in users])  

@api.route('/users/favorites', methods=['GET'])
def get_users_favorites():
    users = User.query.all()  
    return jsonify([user.serialize() for user in users])  

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    user.planet_favorite.append(planet)
    db.session.commit()

    return jsonify({"message": f"Planet {planet.name} added to favorites."}), 201

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    person = Person.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    user.person_favorite.append(person)
    db.session.commit()

    return jsonify({"message": f"Person {person.name} added to favorites."}), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    if planet in user.planet_favorite:
        user.planet_favorite.remove(planet)
        db.session.commit()
        return jsonify({"message": f"Planet {planet.name} removed from favorites."}), 200
    else:
        return jsonify({"error": "Planet not in user's favorites"}), 404

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    person = Person.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    if person in user.person_favorite:
        user.person_favorite.remove(person)
        db.session.commit()
        return jsonify({"message": f"Person {person.name} removed from favorites."}), 200
    else:
        return jsonify({"error": "Person not in user's favorites"}), 404
