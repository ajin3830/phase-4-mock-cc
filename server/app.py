#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

# GET /heroes
@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = Hero.query.all()
    return make_response([hero.to_dict() for hero in heroes], 200)

# GET /heroes/int:id
@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if not hero:
        return make_response({"error": "Hero not found"}, 404)
    return make_response(hero.to_dict(), 200)
        
# GET /powers
@app.route('/powers', methods=['GET'])
def powers():
    powers = Power.query.all()
    return make_response([power.to_dict() for power in powers], 200)

# GET, PATCH /powers/int:id
@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return make_response({"error": "Power not found"}, 404)
    else:
        if request.method == 'GET':
            return make_response(power.to_dict(), 200)
        elif request.method == 'PATCH':
            try: 
                for attr in request.get_json():
                    setattr(power, attr, request.get_json()[attr]) 
                db.session.add(power)    
                db.session.commit()
                return make_response(power.to_dict(), 200)
            except ValueError:
                return make_response({"error": "Invalid input"}, 400)


# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    try:
        new_hp = HeroPower(
            strength=request.get_json()['strength'],
            power_id=request.get_json()['power_id'],
            hero_id=request.get_json()['hero_id']
        )
        db.session.add(new_hp)
        db.session.commit()

        hero = Hero.query.filter_by(id=new_hp.hero_id).first()
        return make_response(hero.to_dict(), 201)
    except ValueError:
        return make_response({"error": "Invalid input"}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
