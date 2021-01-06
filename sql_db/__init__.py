import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import random
from settings import db_url
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()


# db connection string formats
# mssql (using pymssql)
# mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8

# postgresql
# postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]

# mysql
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

# sqlite
# sqlite+pysqlite:///file_path


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_all():
    db.drop_all()
    db.session.commit()


def db_create_all():
    # engine = create_engine(db_url())
    # print(engine.url)
    # if not database_exists(engine.url):
    #     create_database(engine.url)
    db.create_all()
    db.session.commit()


class Test(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
