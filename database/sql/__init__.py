from sqlalchemy import create_engine
import json, os, random
from sqlalchemy_utils import database_exists, create_database, drop_database
from database.sql.models import db
from database.sql.dbtype import DBType
from flask_sqlalchemy import SQLAlchemy


# creating connection string for sql connection. And initializes it within app
def setup_sql_db(app, dbtype: DBType, username, password, host, database_name):
    conn = f"{choose_adapter(dbtype)}://{username}:{password}@{host}/{database_name}"
    conn += "?driver=SQL+Server" if dbtype is DBType.MSSQL else ""

    app.config["SQLALCHEMY_DATABASE_URI"] = conn
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db_create_all(conn)


# chooses adapter based on dbtype
def choose_adapter(dbtype: DBType):
    if dbtype is DBType.MSSQL:
        return "mssql+pyodbc"
    elif dbtype is DBType.MYSQL:
        return "mysql+pymysql"
    elif dbtype is DBType.POSTGRESQL:
        return "postgresql"
    return "mssql+pyodbc"

# drops all tables and drops db if it is a unit test
def db_drop_all(testing=False, conn=""):
    db.session.commit()
    db.session.close()
    db.drop_all()
    if testing is True:
        engine = create_engine(conn)
        if database_exists(engine.url):
            print("Dropping DB")
            drop_database(engine.url)

# create db(if not exist) and tables
def db_create_all(conn):
    engine = create_engine(conn)
    # print(engine.url)
    if not database_exists(engine.url):
        print("Creating DB")
        create_database(engine.url)

    db.create_all()
    db.session.commit()
