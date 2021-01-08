### Python-Api

**python-api** is a boilerplate project for creating a rest api with flask easily. it can configured to use various sql databases (*MS SQL, MYSQL, POSTGRESQL etc.*) and MongoDB as a NOSQL database. The project has a built-in encrypted JWT implementation with auth decorator.



##### Installing Dependencies

Although the project can run if the dependencies are installed globally in the host machine using virtual environment is highly recommended.

To create a virtual environment within the project navigate to the project folder with our favorite command line interface tool. Based on the python interpreter we can use these commands to create virtual environment folder. The folder will be ignored on commits.

```
python3 -m venv env
```

or

```
python -m venv env
```

After creating virtual environment folder we should activate it with using these commands.

For Windows

```
env\Scripts\activate.bat
```

For Unix or MacOS

```
source tutorial-env/bin/activate
```

The file path will be shown with (env) prefix on terminal after activating the virtual environment like below.

```
(env) D:\Repo\Python\python-api-boilerplate>

```


After setting up the virtual environment we can install the necessary packages to our project. We can use the below command to install all of our dependencies based on the the text file within the project.

```
pip install - r requirements.txt
```



### Creating Api Endpoints

To create a public endpoint we can simply use flask decorators.

```
@app.route('/')
 def index():
    return jsonify({
    "message": "Hello World"
})
```

There is a errorhandler.py file within the api module and it returns custom results for frequent http errors. It is added to the pipeline with. 

```
from api.errorhandler import set_handler

app = set_handler(app)

```

With this we will return these errors whenever we use built in abort function of flask with pre created error messages in that file.

```
#this will return the jsonified response from errorhandler.py file
abort(401)
```



###### Secure Endpoints

First we should import necessary functions from the auth module.

```
from auth.auth import requires_auth, create_enc_token, decrypt
```

`create_enc_token` method will create a jwt token for client, create a uid and add that uid to session. And adds the same uid to the claim section of the token to differentiate the clients. 

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

After that client with valid Authorization header will have access to the secure endpoint. 

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



### Database(s) Setup

##### Setup SQL Database

To use the sql database we should import necessary functions from database module

```
from database.sql import setup_sql_db
from database.sql.models import Test
from database.sql.dbtype import DBType
```



`setup_sql_db()`function will set the sql database with given connection information. There is a enum called DBType in the dbtype file. We pass this enum to the function to choose sql database type.

```
setup_sql_db(app, dbtype=DBType.POSTGRESQL, username="<username>", password="<password>",
                 host="<host>", database_name="<dbname>" if test_database is None else test_database)
```

`database.sql.models` contains the models of the database. Test is a model which is created for test purposes. All the models inherits `ModelBase` class which is in the models file too. `ModelBase` class has insert,update and delete methods which is common for all the model classes.

##### Using ModelBase methods for database transactions

Although sqlalchemy supports raw queries we can use ModelBase methods and query mothed for basic transactions by using our model class.

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

Setting up the MongoDB database are pretty much same with setting up the sql database.

```
from database.mongodb import setup_mongodb
```

```
# seting databases
    setup_mongodb(app, username="<username>", password="<password>",
                  host="<host>", database_name="<dbname>" if test_database is None else test_database)
```

We can use sql and mongodb database at the same time. setup_mongodb function will create a database and a default table to ensuring the creation of the database if the database does not exist.

`setup_mongodb`function adds a mongo objects to the app object which we can use to do MongoDB transactions. All of the filter parameters are optional but we can use it if we want to return specific columns.

```
#insert (pass a dictionary to add to the collection)
app.mongo.insert_row(table_name="TestTable" row={name:"Test42"})

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



We can use `mongodb_test.py` and `sql_test.py` files to test our databases.

For both database types our user needs to have permission to create databases. The test files will create a test database. Test that database with test functions and drop the database at the end of the process. I'll change this to mock databases in the future.

To test the database functions we should have been called the necessary function in the api module based on which database we want to test(`setup_sql_db` or `setup_mongodb` or ***both***). Otherwise the tests will fail

To test the databases we can use below commands

```
#for testing mongodb
python -m unittest discover -p mongodb_test.py

#for testing sqldb
python -m unittest discover -p sql_test.py

```



