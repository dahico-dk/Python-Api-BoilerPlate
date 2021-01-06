import pymongo
from settings import mongodb

"mongodb+srv://dhc:6cILUsDI3BBIPeHn@cluster0.ubhyi.mongodb.net/?retryWrites=true&w=majority"


def setup_mongodb(app, username, password, host, database_name):
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class MongoLayer:

    def __init__(self, username, password, host, database_name):
        self.uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.uri)
        self.database_name = database_name
        dblist = self.client.list_database_names()
        if dbname not in dblist:
            people_collection = self.gettable(dbname, "init_collection")
            result = people_collection.insert_one({"name": "Terry Pratchett"})

    def copy_db(self, source_db, target_db):
        self.client.admin.command('copydb',
                                  fromdb=source_db,
                                  todb=target_db)

    def gettable(self, table_name, db_name):
        db = self.client[db_name]
        coll = db[table_name]
        return coll

    def insert_row(self, table_name, row: dictionary, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        inst = coll.insert_one(row)
        return inst.inserted_id

    def bulk_insert(self, table_name, rows: list[dictionary], db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        inst = coll.insert_many(rows)
        return inst.inserted_ids

    def findbyid(self, table_name, id, filter: dictionary = {}, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.find_one({"_id", id}, filter)

    def findone(self, table_name, query: dictionary, filter: dictionary = {}, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.find_one(query, filter)

    def findmany(self, table_name, query: dictionary, filter: dictionary = {}, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.findmany(query, filter)

    def find(self, table_name, query: dictionary = {}, filter: dictionary = {}, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.find(query, filter)

    def deleteone(self, table_name, query: dictionary, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.deleteone(query)

    def deletemany(self, table_name, query: dictionary, db_name=self.database_name):
        coll = self.gettable(table_name, db_name)
        return coll.deletemany(query)
