# Python-Api-BoilerPlate

**python-api** is a boilerplate project for creating a rest api with flask easily. it can configured to use various sql databases (*MS SQL, MYSQL, POSTGRESQL etc.*) and MongoDB as a NOSQL database. The project has a built-in encrypted JWT implementation with auth decorator.

## Getting Started

#### Installing Dependencies

#### Python

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Although the project can run if the dependencies are installed globally using virtual environment is highly recommended. This keeps dependencies for each project separate and organized. 

Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once virtual environment has been set and running, dependencies can be installed by running at the root directory 

```
pip install - r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM which will be used for handling the sql database. [Flask-SQLAlchemy](https://readthedocs.org/projects/flask-sqlalchemy/) will be the wrapper.
- [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/en/latest/) is the module for creating and dropping databases. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests. 
- [JWCrypto](https://jwcrypto.readthedocs.io/en/latest/) is the module we will use for creating encrypted jwt tokens. 
- [Flask-Session](https://flask-session.readthedocs.io/en/latest/) is the module we will use for creating sessions and diferantiate client side for jwt decryption
- [PyMongo](https://readthedocs.org/projects/pymongo/) is the module we will use for interacting with MongoDB database.

### Database Setup

##### Setup SQL Database

To use the SQL database we should import necessary functions from database module within the project.

```
from database.sql.models import Test
from database.sql.dbtype import DBType
from database.sql import setup_sql_db
```

- ***database.sql.models*** contains the models of the database. Test is a model which is created for test purposes. All the models inherits `ModelBase` class which is in the models file too. `ModelBase` class has insert,update and delete methods which is common for all the model classes..
- ***database.sql.dbtype*** is the enum for database type. We pass this enum to the function to choose SQL database type.
- ***database.sql*** module contains functions for setup, create and drop functions for database. `setup_sql_db()`function sets up the connection string as can be seen in the code below.

```
setup_sql_db(app, dbtype=DBType.POSTGRESQL, username="<username>", password="<password>",
                 host="<host>", database_name="<dbname>" if test_database is None else test_database)
```

###### *ModelBase inheritance*

The models which inherits the ModelBase class can use the ***insert, delete, update*** functions for basic transaction.

```
class Test(db.Model, ModelBase):
    def __init__(self, title):
        self.title = title
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
```

###### *Using ModelBase methods for database transactions*

Although *SQLALCHEMY* supports raw queries we can use *ModelBase* methods and query method for basic transactions by using our model class.

```
#Select
Test.query.filter_by(id=42).first()
#insert
test = Test(title="Test42")
test.insert()
#update
test=Test.query.filter_by(id=42).first()
test.title="Test42"
test.update()
#delete
test=Test.query.filter_by(id=42).first()
test.delete()
```

##### Setup MongoDB Database

Setting up the MongoDB database is pretty much same with setting up the SQL database process.

```
from database.mongodb import setup_mongodb
```

```
# seting databases
    setup_mongodb(app, username="<username>", password="<password>",
                  host="<host>", database_name="<dbname>" if test_database is None else test_database)
```

We can use SQL and MongoDB database at the same time. `setup_mongodb` function will create a database and a default table *(init_collection)* to ensuring the creation of the database if the database does not exist.

`setup_mongodb` function adds a mongo objects to the app object which we can use for MongoDB transactions. All of the filter parameters are optional but we can use it if we want to return specific columns from the query. Also we can pass a *<u>db_name</u>* parameter to the functions for using it with another database. Otherwise the module will use the database specified with `setup_mongodb` function.

###### Using mongo object functions for transactions

```
#insert (pass a dictionary to add to the collection)
app.mongo.insert_row(table_name="TestTable" row={name:"Test42"})

#insert (pass a dictionary to add to the collection for another database)
app.mongo.insert_row(table_name="TestTable" row={name:"Test42"}, db_name="Another Database")

#bulk insert
app.mongo.bulk_insert(table_name="TestTable", rows=[{name:"Test42"},{name:"Test42"}])

#find one by id (filter is optional. Below query will only return _id)
app.mongo.findbyid(table_name="TestTable", id=inserted,filter={'_id': 1})

#find one  by prop (will return rows with name equals Test42.Filter is optional )
app.mongo.findone(table_name="TestTable", query={name:"Test42"},filter={'_id': 1,'name':1})

#find all by prop (filter is optional)
app.mongo.find(table_name="TestTable", query={name:"Test42"},filter={'_id': 1,'name':1})

#delete one by id
app.mongo.deletebyid(table_name="TestTable", id="507f1f77bcf86cd799439011")

#delete many by query. Below code deletes all with the name Test42.
app.mongo.deletemany(table_name="TestTable", query={name:"Test42"})

#update by id (updates the row with with newval)
app.mongo.updatebyid(table_name="TestTable", id="507f1f77bcf86cd799439011", newval={"name": "Test42"})

#update one by query
app.mongo.updateone(table_name="TestTable", query={name:"Test42"}, newval={"name": "Test42"})

#update many by query (updates all rows with name Test42)
app.mongo.updatemany(table_name="TestTable", query={name:"Test42"}, newval={"name": "Test42"})

```

### Testing the Database Settings

`mongodb_test.py` and `sql_test.py` files can be used to test the databases. These files tests the transaction methods for the given databases.

For both database types the user needs to have permission for creating databases. The test files will create a test database. Test that database with test functions and drop the database at the end of the process. This will be changed to use mock databases in the future.

To test the database functions first we should call the necessary functions in the api module based on which database we want to test (`setup_sql_db` or `setup_mongodb` or ***both***). Otherwise the tests will fail.

To test the databases we can use below commands

```
#for testing mongodb
python -m unittest discover -p mongodb_test.py

#for testing sqldb
python -m unittest discover -p sql_test.py

```

### Creating Api Endpoints

To create a public endpoint we can simply use *Flask* decorators.

```
@app.route('/')
 def index():
    return jsonify({
    "message": "Hello World"
})

@app.route('/other_endpoint')
 def some_other_endpoint():
    return jsonify({
    "message": "Hello Tatooine"
})
```

###### Error Handling

Errors are returned as JSON objects in the following format.

```
{
       "error": 404,
       "message": "resource not found",
       "success": False
}
```

There is a errorhandler.py file within the api module and it returns custom results for frequent http errors. It is added to the pipeline with. 

```
from api.errorhandler import set_handler

app = set_handler(app)
```

With this we will return these json object errors whenever we use built in abort function of Flask with pre created error messages in that file.

```
#this will return the jsonified response from errorhandler.py file
abort(401)
```

This module returns eight error types 

- 404:Not Found
- 401:Unauthorized
- 405:Method not allowed
- 422:Not Processable
- 413:Payload Too Large
- 429:Too Many Requests
- 403:Forbidden
- AUTH Error: Custom Error for Authorization failures

##### Secure Endpoints

To create secure endpoints we should import necessary functions from the auth module.

```
from auth.auth import requires_auth, create_enc_token, decrypt
```

`create_enc_token` method will create a JWT token for client, create and add that UUID to session. And adds the same UUID to the claim section of the token to differentiate the clients. 

```
	key = jwk.JWK(generate='oct', size=256)
    uid = str(uuid.uuid4())
    set_key(key.export(), uid)
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"uid": uid})
    token.make_signed_token(key)
    etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                     claims=token.serialize())
    etoken.make_encrypted_token(key)
    return etoken.serialize()
```

And we will pass this token to the client.

```
 	# public api endpoint. Creates a encrypted jwt token
    @app.route('/api/public')
    def public_url():
        return jsonify({
            "message": "this is a public url.",
            "token": str(create_enc_token())
        })
```

After that client with valid Authorization header will have access to the secure endpoints within the same session. `requires_auth` is the decorator we use for validating tokens. It will throw a 401 error on fail.

```
 	# private endpoint. Will throw 401 if token is not right
    @app.route('/api/restricted')
    @requires_auth()
    def restricted():
        return jsonify({
            "message": "this is a restricted url.",
        })
```

Auth module will called by decorator and decrypt the token . And compare the uid claim with the session.

```
# returns true or false. Compares uid with the payload
def decrypt(e):
    key, uid = get_key()
    ikey = jwk.JWK(**json.loads(key))
    et = jwt.JWT(key=ikey, jwt=e)
    st = jwt.JWT(key=ikey, jwt=et.claims)
    stdict = json.loads(st.claims)
    return stdict.get("uid")
```

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

- For Linux and MacOS

```bash
export FLASK_APP=api
export FLASK_ENV=development
flask run
```

- For Windows

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `api` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

