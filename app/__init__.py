from flask import Flask, jsonify, abort
from flask_cors import CORS
from auth.auth import requires_auth, create_ enc_token, decrypt
from flask_session import Session
from app.errorhandler import set_handler
import uuid
from database.sql import db_create_all, db_drop_all, Test, setup_sql_db
from database.sql import DBType
from database.sql import Test
from database.mongodb import MongoLayer


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.secret_key = "F*q}/{QAKpF:M,Z3W7zBN2n0MV@}m;VLz)*!o'),;-MiX" + str(uuid.uuid4())
    app = set_handler(app)
    setup_sql_db(app, dbtype=DBType.MSSQL, username="hakkisagdic", password="kodluyoruz.!2020",
                 host="kodluyoruz.database.windows.net: 1433", database_name="daghaninki")
    db_create_all()

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/')
    def index():
        return jsonify({
            "message": "Hello World"
        })

    @app.route('/api/public')
    def public_url():
        return jsonify({
            "message": "this is a public url.",
            "token": str(create_enc_token())
        })

    @app.route('/api/restricted')
    @requires_auth()
    def restiricted():
        return jsonify({
            "message": "this is a restricted url.",
        })

    if __name__ == 'main':
        sess = Session()
        sess.init_app(app)

    return app
