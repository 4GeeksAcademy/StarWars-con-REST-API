from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    people = db.relationship('People', backref="User", lazy=True)
    planets = db.relationship('Planets', backref="User", lazy=True)
    favoritos_people = db.relationship('FavoritosPeople', backref="User", lazy=True)
    favoritos_planets = db.relationship('FavoritosPlanets', backref="User", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'People'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    homeworld = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    favoritos_people = db.relationship('FavoritosPeople', backref="People", lazy=True)

    def __init__(self, name, description, gender, birth_year, homeworld, user_id):
        self.name = name
        self.description = description
        self.gender = gender
        self.birth_year = birth_year
        self.homeworld = homeworld 
        self.user_id = user_id
        self.creation_date = date.today()

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld,
            "user_id": self.user_id,
            "creation_date": self.creation_date,
        }

class Planets(db.Model):
    __tablename__ = 'Planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    favoritos_planets = db.relationship('FavoritosPlanets', backref="Planets", lazy=True)


    def __init__(self, name, description, climate, terrain, population, gravity, diameter, user_id):
        self.name = name
        self.description = description
        self.climate = climate
        self.terrain = terrain
        self.population = population
        self.gravity = gravity
        self.diameter = diameter
        self.user_id = user_id
        self.creation_date = date.today()

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "user_id": self.user_id,
            "creation_date": self.creation_date,
        }

class FavoritosPeople(db.Model):
    __tablename__ = 'FavoritosPeople'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("People.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

class FavoritosPlanets(db.Model):
    __tablename__ = 'FavoritosPlanets'
    id = db.Column(db.Integer, primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey("Planets.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)