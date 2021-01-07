from flask import Flask, jsonify, abort
from flask_cors import CORS
from auth.auth import requires_auth, create_enc_token, decrypt
from flask_session import Session
from api.errorhandler import set_handler
import uuid
from database.sql import db_create_all, db_drop_all, setup_sql_db
from database.sql.models import Test
from database.sql.dbtype import DBType
from database.mongodb import MongoLayer, setup_mongodb
from flask_migrate import Migrate


def create_app(test_config=None, test_database=None):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # for session diferantiate
    app.secret_key = str(uuid.uuid4())
    app = set_handler(app)

    # # seting databases
    # setup_mongodb(app, username="<username>", password="<password>",
    #               host="<host>", database_name="<dbname>" if test_database is None else test_database)

    setup_sql_db(app, dbtype=DBType.POSTGRESQL, username="postgres", password="1234",
                 host="localhost:5432", database_name="<dbname>" if test_database is None else test_database)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    # public api endpoint
    @app.route('/')
    def index():
        return jsonify({
            "message": "Hello World"
        })

    # public api endpoint. Creates a encrypted jwt token
    @app.route('/api/public')
    def public_url():
        return jsonify({
            "message": "this is a public url.",
            "token": str(create_enc_token())
        })

    # private endpoint. Will throw 401 if token is not right
    @app.route('/api/restricted')
    @requires_auth()
    def restricted():
        return jsonify({
            "message": "this is a restricted url.",
        })

    if __name__ == 'main':
        sess = Session()
        sess.init_app(app)
    return app
