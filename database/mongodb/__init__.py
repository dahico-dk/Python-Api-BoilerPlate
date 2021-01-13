import pymongo
from bson.objectid import ObjectId


def setup_mongodb(app, username, password, host, database_name):
    app.mongo = MongoLayer(username, password, host, database_name)


class MongoLayer:
    """
    creates mongodb uri and creates a test collection to create the database.
    """

    def __init__(self, username, password, host, database_name):
        self.uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.uri)
        self.database_name = database_name
        dblist = self.client.list_database_names()
        if database_name not in dblist:
            # avoiding lazy db creation by forcing a collection create while honoring my favourite author
            test_coll = self.gettable("init_collection", db_name=database_name)
            result = test_coll.insert_one({"name": "Terry Pratchett"})

    def copy_db(self, source_db, target_db):
        self.client.admin.command('copydb',
                                  fromdb=source_db,
                                  todb=target_db)

    def gettable(self, table_name, db_name=None):
        db = self.client[db_name if db_name is not None else self.database_name]
        coll = db[table_name]
        return coll

    # basic transaction methods

    def insert_row(self, table_name, row: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        inst = coll.insert_one(row)
        return inst.inserted_id

    def bulk_insert(self, table_name, rows: list, db_name=None):
        coll = self.gettable(table_name, db_name)
        inst = coll.insert_many(rows)
        return inst.inserted_ids

    def findbyid(self, table_name, id, filter: dict = None, db_name=None):
        coll = self.gettable(table_name, db_name)
        ret = coll.find({"_id": id}, filter)
        if ret.count() > 0:
            return ret[0]
        else:
            return None

    def findone(self, table_name, query: dict = {}, filter: dict = None, db_name=None):
        coll = self.gettable(table_name, db_name)
        ret = coll.find(query, filter)
        if ret.count() > 0:
            return ret[0]
        else:
            return None

    def find(self, table_name, query: dict = {}, filter: dict = None, db_name=None):
        coll = self.gettable(table_name, db_name)
        return coll.find(query, filter)

    def deletebyid(self, table_name, id, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.delete_one({"_id": id})

    def deleteone(self, table_name, query: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.delete_one(query)

    def deletemany(self, table_name, query: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.delete_many(query)

    def dropcoll(self, table_name, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.drop()
        return True

    def updatebyid(self, table_name, id, newval: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.update_one({"_id": id}, {"$set": newval})
        return True

    def updateone(self, table_name, query: dict, newval: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.update_one(query, {"$set": newval})
        return True

    def updatemany(self, table_name, query: dict, newval: dict, db_name=None):
        coll = self.gettable(table_name, db_name)
        coll.update_many(query, {"$set": newval})
        return True
