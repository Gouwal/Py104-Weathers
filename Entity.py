from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neil:mypass@localhost/postgres'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Weathers_xz(db.Model):
    __tablename__ = 'Tianqi_xz'


    Id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), primary_key=True)
    day = db.Column(db.String(64))
    weather = db.Column(db.String(64))
    temperature = db.Column(db.String(64))

if __name__ == '__main__':
    manager.run()
