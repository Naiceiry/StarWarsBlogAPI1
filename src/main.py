"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import Peoples, Planets, FavoritePeoples, FavoritePlanets, UserFavorites

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejar / serializar errores como un objeto JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generar mapa del sitio con todos sus puntos finales
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=["GET"])
def get_all_peoples():

    peoples_list = []
    response_list = Peoples.query.all()
    
    for people in response_list:
        peoples_list.append(people.serialize())
    
    if len(peoples_list) > 0:
        return jsonify(peoples_list), 200
    else:
        return "People not found", 404
 
# [GET] /people/<int:people_id>Obtener información de una sola persona
@app.route('/people/<int:url>', methods=["GET"])
def get_people_By_id(url):
    result = next((people for people in peoples_list if people["url"] == url), None)
    if result is not None:
        return jsonify(result), 200
    else:
        return "People not found", 404

# [GET] /planets Obtenga una lista de todos los planetas en la base de datos
@app.route('/planet', methods=["GET"])
def get_all_planets():
    planets_list = []
    response_list = Planets.query.all()
    
    for planet in response_list:
        planets_list.append(planet.serialize())
    
    if len(planets_list) > 0:
        return jsonify(planets_list), 200
    else:
        return "Planet not found", 404
 
    
   
# [GET] /planets/<int:planet_id> Obtenga información sobre un solo planeta
@app.route('/planet/<int:url>', methods=["GET"])
def get_planet_By_id(url):
    result = next((planet for planet in planets_list if planet["url"] == url), None)
    if result is not None:
        return jsonify(result), 200
    else:
        return "Planet not found", 404

# [GET] /users Obtenga una lista de todos los usuarios de publicaciones de blog

@app.route('/user', methods=["GET"])
def get_all_users():
    users_list = []
    response_list = User.query.all()
    
    for user in response_list:
        users_list.append(user.serialize())
    
    if len(users_list) > 0:
        return jsonify(users_list), 200
    else:
        return "User not found", 404

# [GET] /users/favorites Get all the favorites that belong to the current user.
@app.route('/user/favorites', methods=["GET"])
def get_user_favorites():
    user_favorites_list = []
    response_list = UserFavorites.query.all()
    
    for people in response_list:
        user_favorites_list.append(userFavorites.serialize())
    
    if len(user_favorites_list) > 0:
        return jsonify(user_favorites_list), 200
    else:
        return "User favorits not found", 404

# [POST] /favorite/planet/<int:url> Agregue un nuevo  favorito al usuario actual con el url = url.
@app.route('/favorite/planet/<int:url> ', methods=["POST"])
def favorite_planets_list():
    body_request = request.get_json()
    favourite_list = []
    
    user_id_request = body_request.get("user_id", None)
    id_request = body_request.get("url", None)
        
    favourite_list = FavoritePlanets(
      user_id = user_id_request,
      planet_id = planet_id_request
    )

    db.session.add(favourite_list)
    db.session.commit()
    return jsonify(favourite_list.serialize()), 201

# [POST] /favorite/people/<int:people_id> Agregue nuevas personas favoritas al usuario actual con url= url
@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def favorite_peoples_list():
    body_request = request.get_json()
    favourite_list = []
    
    user_id_request = body_request.get("user_id", None)
    people_id_request = body_request.get("peoples_id", None)
        
    favourite_list = FavoritePeoples(
      user_id = user_id_request,
      peoples_id = peoples_id_request
    )

    db.session.add(favourite_list)
    db.session.commit()
    return jsonify(favourite_list.serialize()), 201

# [DELETE] /favorite/planet/<int:planet_id> Elimina el planeta favorito con id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=["DELETE"])
def delete_favorite_planet():
    body_request = request.get_json()
    favourite_list = []
    
    user_id_request = body_request.get("user_id", None)
    planet_id_request = body_request.get("planet_id", None)
        
    delete_favorite_planet = FavoritePlanets.query.filter_by(user_id = user_id_request, planet_id = planet_id_request).first_or_404()

    try:
        db.session.delete(delete_favorite_planet)
        db.session.commit()
        return jsonify({"msg":"Planet Successfully Deleted "}), 200
            
    except:
        return "ERROR PLANET NOT DELETED", 400

# [DELETE] /favorite/people/<int:people_id> Elimina las personas favoritas con id = people_id.
@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_favorite_people():
    body_request = request.get_json()
    favourite_list = []
    
    user_id_request = body_request.get("user_id", None)
    people_id_request = body_request.get("peoples_id", None)   
    delete_favorite_people = FavoritePeoples.query.filter_by(user_id = user_id_request, peoples_id = people_id_request).first_or_404()

    try:
        db.session.delete(delete_favorite_people)
        db.session.commit()
        return jsonify({"msg":"People Successfully Deleted "}), 200
            
    except:
        return "ERROR PEOPLE NOT DELETED", 400


# esto solo se ejecuta si se ejecuta `$ python src / main.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=true)