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
from models import db, User, People, Planets, FavoritosPlanets, FavoritosPeople
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

@app.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    print(all_users)
    return jsonify([user.serialize() for user in all_users]), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    print(all_people)
    return jsonify([people.serialize() for people in all_people]), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    print(all_planets)
    return jsonify([planet.serialize() for planet in all_planets]), 200

@app.route('/new-people', methods=['POST'])
def new_people():
    body = request.json  
    try:
        new_people = People(body['name'], body['description'], body['gender'],
                            body['birth_year'], body['homeworld'], body['user_id'])
      
        print(new_people)
        db.session.add(new_people)  
        db.session.commit()
        return jsonify(new_people.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
@app.route('/new-planet', methods=['POST'])
def new_planet():
    body = request.json  
    try:
        new_planet = Planets(body['name'], body['description'], body['climate'],
                            body['terrain'], body['population'], body['gravity'],
                            body['diameter'], body['user_id'])
      
        print(new_planet)
        db.session.add(new_planet)  
        db.session.commit()
        return jsonify(new_planet.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
@app.route('/people/<id>', methods=['GET'])
def get_detailsPeople(id):
    try:
        infoPeople = People.query.filter_by(id=id).one_or_none()
        people = infoPeople.serialize()
        return jsonify({"people": people}), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/planets/<id>', methods=['GET'])
def get_detailsPlanet(id):
    try:
        infoPlanet = Planets.query.filter_by(id=id).one_or_none()
        planet = infoPlanet.serialize()
        return jsonify({"planet": planet}), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorito-people', methods=['POST'])
def setFavoritoPeople():
    body = request.json  
    try:
        new_favoritoPeople = FavoritosPeople(body['people_id'], body['user_id'])
        print(new_favoritoPeople)
        db.session.add(new_favoritoPeople)  
        db.session.commit()
        return jsonify(new_favoritoPeople.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500


@app.route('/favorito-people', methods=['DELETE'])
def deleteFavoritoPeople():
    body = request.json  
    try:
        aux_favoritoPeople = FavoritosPeople.query.filter_by(
            people_id=body['people_id'], user_id=body['user_id']).one_or_none()
        print(aux_favoritoPeople)
        db.session.delete(aux_favoritoPeople)  
        db.session.commit()
        return jsonify(aux_favoritoPeople.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
@app.route('/favorito-planets', methods=['POST'])
def setFavoritoPlanets():
    body = request.json  
    try:
        new_favoritoPlanet = FavoritosPlanets(body['planets_id'], body['user_id'])
        print(new_favoritoPlanet)
        db.session.add(new_favoritoPlanet)  
        db.session.commit()
        return jsonify(new_favoritoPlanet.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500


@app.route('/favorito-planets', methods=['DELETE'])
def deleteFavoritoPlanet():
    body = request.json  
    try:
        aux_favoritoPlanet = FavoritosPlanets.query.filter_by(
            planets_id=body['planets_id'], user_id=body['user_id']).one_or_none()
        print(aux_favoritoPlanet)
        db.session.delete(aux_favoritoPlanet)  
        db.session.commit()
        return jsonify(aux_favoritoPlanet.serialize()), 200
    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
@app.route('/favorito-people/<idUser>', methods=['GET'])
def get_AllFavoritosPeopleUser(idUser):
    try:
        listPeople = FavoritosPeople.query.filter_by(
            user_id=idUser).all()
        return jsonify([people.serialize() for people in listPeople]), 200

    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@app.route('/favorito-planets/<idUser>', methods=['GET'])
def get_AllAllFavoritosPlanetsUser(idUser):
    try:
        listPlanets = FavoritosPlanets.query.filter_by(
            user_id=idUser).all()
        return jsonify([planet.serialize() for planet in listPlanets]), 200

    except Exception as err:
        return jsonify({"message": "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
