#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Villain, HeroVillain

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"


@app.get('/debug')
def debug():
    import ipdb; ipdb.set_trace()
    return "Debugging! Yay!"


# INDEX #
@app.get('/heroes')
def all_heroes():
    heroes = Hero.query.all()
    heroes_to_dict = [ hero.to_dict() for hero in heroes ]
    return heroes_to_dict, 200

# SHOW #
@app.get('/heroes/<int:id>')
def hero_by_id(id):
    try:
        hero = Hero.query.filter(Hero.id == id).first()
        return hero.to_dict(), 200
    except Exception as e:
        return { "error": "404 Not found" }, 404


# INDEX #
@app.get('/villains')
def all_villains():
    villains = Villain.query.all()
    villains_to_dict = [ villain.to_dict(rules=('heroes',)) for villain in villains ]
    return villains_to_dict, 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)
