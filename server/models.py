from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    power = db.Column(db.String)
    weakness = db.Column(db.String)

    herovillains = db.relationship('HeroVillain', back_populates='hero')

    villains = association_proxy('herovillains', 'villain')

    serialize_rules = ('-herovillains', 'villains', '-villains.heroes', '-villains.herovillains')


class Villain(db.Model, SerializerMixin):
    
    __tablename__ = 'villains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    secret_lair = db.Column(db.String)
    childhood_trauma = db.Column(db.String)

    herovillains = db.relationship('HeroVillain', back_populates='villain')

    heroes = association_proxy('herovillains', 'hero')

    serialize_rules = ('-herovillains.villain',)

    
class HeroVillain(db.Model, SerializerMixin):

    __tablename__ = 'herovillains'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    villain_id = db.Column(db.Integer, db.ForeignKey('villains.id'))

    # RELATIONSHIPS #

    hero = db.relationship('Hero', back_populates='herovillains')
    villain = db.relationship('Villain', back_populates='herovillains')

    serialize_rules = ('-hero.herovillains', '-villain.herovillains')
    