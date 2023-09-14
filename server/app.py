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


# VILLAINS #
# CREATE / READ / UPDATE / DELETE

# CREATE
@app.post('/villains')
def create_villain():
    villain_data = request.json

    villain = Villain( name = villain_data["name"], secret_lair = villain_data["secret_lair"], childhood_trauma = villain_data["childhood_trauma"] )

    db.session.add( villain )
    db.session.commit()

    return villain.to_dict(), 201


# READ ALL
@app.get('/villains')
def all_villains():
    villains = Villain.query.all()
    villains_list = [ villain.to_dict(rules=("-herovillains",)) for villain in villains ]
    return villains_list, 200


# READ BY ID
@app.get('/villains/<int:id>')
def villain_by_id(id):
    try:
        villain = Villain.query.where(Villain.id == id).first()
        return villain.to_dict(), 200
    except AttributeError:
        return { "error": "404 Not Found" }, 404


# UPDATE BY ID
@app.patch('/villains/<int:id>')
def update_villain(id):
    data_to_update = request.json
    Villain.query.where(Villain.id == id).update(data_to_update)
    db.session.commit()
    villain = Villain.query.where(Villain.id == id).first()
    return villain.to_dict(), 202


# DELETE
@app.delete('/villains/<int:id>')
def delete_villain(id):
    try:
        villain = Villain.query.where(Villain.id == id).first()
        db.session.delete( villain )
        db.session.commit()
        return {}, 204
    except:
        return {"error": "404 Could not delete, not found" }, 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
