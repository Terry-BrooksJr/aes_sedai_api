from turtle import position
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
import os


#* Intalize App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aes_sedai_api.db')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API.'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404

#* Models for Database

class AesSedai(db.Model):
    __tablename__ = 'aes_sedai'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    home_country = Column(String)
    ajah = Column(String)
    position = Column(String)
    warder = Column(Integer, ForeignKey(Warder.id))
    

class Ashaman(db.Model):
    __tablename__ = 'ashaman'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    home_country = Column(String)
    position = Column(String)
    

class Warder(db.Model):
    __tablename__ = 'warder'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    home_country = Column(String)
    position = Column(String)
    aes_sedai = Column(Integer, ForeignKey(AesSedai.id))
    

#* Database CLI Scripts
#* Intalize Database
db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Boom DB ready')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Poof! DB Gone')


@app.cli.command('db_seed')
def db_seed():
    suian = AesSedai(
        first_name="Suian",
        last_name="Sanche",
        home_country="Tear",
        position="Amrylin Seat")

    merlilla = Warder(
        first_name="Avion",
        last_name="Unknown",
        home_country="Unknown",
        position="Primary Green Warder")

    logain = Ashaman(
        first_name="Logain",
        last_name="Ablar",
        home_country="Gheldan",
        position="Mahalel")

    db.session.add(suian)
    db.session.add(merlilla)
    db.session.add(logain)
    print('BAM DB Seeded')


if __name__ == '__main__':
    app.run()
