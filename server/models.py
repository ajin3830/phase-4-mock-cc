from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata = metadata)

# db = SQLAlchemy()

# 2nd Attempt

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    # serialize_rules = ('-powers.heroes', '-hero_powers' )   
    # This doesn't work! Can't have '-hero_powers' here, you'll get this error
    # FAILED ../Flask application in app.py creates one hero_power using a strength, 
    # a hero_id, and a power_id with a POST request to /hero_powers. 
    # - KeyError: 'hero_powers'

    # # many powers have many heroes 
    serialize_rules = ('-hero_powers.power', "-hero_powers.hero")
    # These all work as well!
    # serialize_rules = ('-powers.heroes',)   
    # serialize_rules = ('-hero_powers.hero', '-powers.heroes')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship
    hero_powers = db.relationship('HeroPower', backref='hero')
    # association
    powers = association_proxy('hero_powers', 'power')

    def __repr__(self):
        return f'<Hero {self.name} />'
    
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    # many heroes have many powers
    serialize_rules = ("-hero_powers.power", "-hero_powers.hero")
    # serialize_rules = ('-heroes.powers', '-hero_powers')   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship
    hero_powers = db.relationship('HeroPower', backref='power')
    # association
    heroes = association_proxy('hero_powers', 'hero')

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError('description must be present and at least 20 characters long')
        return description
    
    def __repr__(self):
        return f'<Power {self.name} />'
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    # one to many singular to plural
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')   
    # serialize_rules = ('-hero.hero_powers', "-power.hero_powers", "-heroes.powers", "-powers.heroes")


    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship columns
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    @validates('strength')
    def validate_strength(self, key, strength):
        values = ['Strong', 'Weak', 'Average']
        if strength not in values:
            raise ValueError('strength must be one of the following values: "Strong", "Weak", "Average"')
        return strength
    
    def __repr__(self):
        return f'<HeroPower {self.strength} />'
