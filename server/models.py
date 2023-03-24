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

    serialize_rules = ('-hero_powers.power', "-hero_powers.hero")
    # serialize_rules = ('-hero_powers.hero', '-powers.heroes')


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')

    powers = association_proxy('hero_powers', 'power')

    def __repr__(self):
        return f'<Hero {self.name} {self.super_name} />'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ("-hero_powers.power", "-hero_powers.hero")
    # serialize_rules = ('-hero_powers.power', '-heroes.powers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description)< 20:
            raise ValueError('Must have a description with at least 20 characters long')
        return description

    hero_powers = db.relationship('HeroPower', backref='power')

    heroes = association_proxy('hero_powers', 'hero')

    def __repr__(self):
        return f'<Power {self.name} {self.description} />'
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    # one to many singular to plural
    serialize_rules = ('-hero.hero_powers', "-power.hero_powers", "-heroes.powers", "-powers.heroes")

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())   

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    @validates('strength')
    def validate_strength(self, key, strength):
        # if not strength =='Strong' and not strength =='Weak' and not strength == 'Average'
        values = ['Strong', 'Weak', 'Average']
        if strength not in values:
            raise ValueError('Must be strong, weak, or average')
        return strength
    
    def __repr__(self):
        return f'<HeroPower {self.strength} />' 