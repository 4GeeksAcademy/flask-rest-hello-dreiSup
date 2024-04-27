"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#get user

@app.route('/user', methods=['GET'])
def handle_user():

    response_body = {}
    user = User.query.all()
    response_body['results'] = [row.serialize() for row in user]
    response_body['message'] = 'Method GET User'
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_single_user(user_id):

    response_body = {}
    user = User.query.get(user_id)
    response_body['results'] = [user.serialize()]
    response_body['message'] = 'Method GET User'
    return jsonify(response_body), 200

#planets
@app.route('/planets', methods=['GET'])
def get_planets():

    response_body = {}
    planets = Planets.query.all()
    response_body['results'] = [row.serialize() for row in planets]
    response_body['message'] = 'Method GET Planets'
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_single_planet(planets_id):

    response_body = {}
    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify('planet does not exist'), 400
    response_body['results'] = [planet.serialize()]
    response_body['message'] = 'Method GET User'
    return jsonify(response_body), 200

#characters
@app.route('/characters', methods=['GET'])
def get_characters():

    response_body = {}
    characters = Characters.query.all()
    response_body['results'] = [row.serialize() for row in characters]
    response_body['message'] = 'Method GET Characters'
    return jsonify(response_body), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_single_character(characters_id):

    response_body = {}
    character = Characters.query.get(characters_id)
    if not character:
        return jsonify('character does not exist'), 400
    response_body['results'] = [character.serialize()]
    response_body['message'] = 'Method GET User'
    return jsonify(response_body), 200

#--------------------------- favorites -------------------------------
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    response_body = {}
    user = User.query.get(user_id)
    if not user:
        return jsonify('user does not exist'), 400
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    response_body['results'] = [row.serialize() for row in favorites]
    response_body['message'] = 'method GET favorites'
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods = ['POST'])
def post_fav_planets_foruser(user_id, planet_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify('user does not exist'), 400
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify('planet does not exist or other error idk'), 200
    favorite = Favorites (user_id = user_id , planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {'msg':'planet added to favorites'}
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods = ['POST'])
def post_fav_character_foruser(user_id, character_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify('user does not exist'), 400
    character = Characters.query.get(character_id)
    if not character:
        return jsonify('character does not exist or other error idk'), 200
    favorite = Favorites (user_id = user_id , character_id = character_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {'msg':'character added to favorites'}
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods = ['DELETE'])
def delete_fav_planets_foruser(user_id, planet_id):
    
    favorite = Favorites.query.filter_by (user_id = user_id , planet_id = planet_id).first()
    db.session.delete(favorite)
    db.session.commit()
    response_body = {'msg':'planet deleted from favorites'}
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods = ['DELETE'])
def delete_fav_characters_foruser(user_id, character_id):
    
    favorite = Favorites.query.filter_by (user_id = user_id , character_id = character_id).first()
    db.session.delete(favorite)
    db.session.commit()
    response_body = {'msg':'character deleted from favorites'}
    return jsonify(response_body), 200



    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
