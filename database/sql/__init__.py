from sqlalchemy import create_engine
import json, os, random
from settings import db_url
from sqlalchemy_utils import database_exists, create_database
from database.sql.models import db
from database.sql.dbtype import DBType
from flask_sqlalchemy import SQLAlchemy


def setup_sql_db(app, dbtype: DBType, username, password, host, database_name):
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"{choose_adapter(dbtype)}://{username}:{password}@{host}/{database_name}" + "?driver=SQL+Server" if dbtype is DBType.MSSQL else ""
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def choose_adapter(dbtype: DBType):
    if dbtype is DBType.MSSQL:
        return "mssql+pyodbc"
    elif dbtype is DBType.MYSQL:
        return "mysql+pymysql"
    elif dbtype is DBType.POSTGRESQL:
        return "postgresql"
    return "mssql+pyodbc"


def db_drop_all():
    db.drop_all()
    db.session.commit()


def db_create_all():
    engine = create_engine(db_url())
    # print(engine.url)
    if not database_exists(engine.url):
        print("Creating DB")
        create_database(engine.url)

    db.create_all()
    db.session.commit()
