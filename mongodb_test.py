import unittest,pymongo,uuid
from api import create_app



# python -m unittest discover -p mongodb_test.py

class MongoDBTestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = str(uuid.uuid4())[:8]
        cls.app = create_app(test_database="test_" + cls.session)
        cls.database_name = "test_" + cls.session
        cls.table = "ttest_" + cls.session

    # -----------------------------------------------------------test cases ------------------------------------------------------------
    def test_insert_row(self):
        # Arrange
        row = {"name": "Test that!" + self.session}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        # Assert
        self.assertTrue(inserted)

    def test_bulk_insert(self):
        # Arrange
        row = {"name": "Test that!" + self.session}
        # Act
        inserted = self.app.mongo.bulk_insert(table_name=self.table, rows=[row])
        # Assert
        self.assertTrue(inserted)

    def test_findbyid(self):
        # Arrange
        row = {"name": "Test that!" + self.session}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        found = self.app.mongo.findbyid(table_name=self.table, id=inserted)
        # Assert
        self.assertTrue(inserted)
        self.assertEqual(found["_id"], inserted)

    def test_findone(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        row = {"name": name}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        found = self.app.mongo.findone(table_name=self.table, query=row)
        nonqueryfound = self.app.mongo.findone(table_name=self.table)
        # Assert
        self.assertTrue(inserted)
        self.assertEqual(found["name"], name)
        self.assertTrue(len(nonqueryfound) > 0)

    def test_find(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        row = {"name": name}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        found = self.app.mongo.find(table_name=self.table, query=row)
        nonqueryfound = self.app.mongo.find(table_name=self.table)
        # Assert
        self.assertTrue(inserted)
        self.assertEqual(found[0]["name"], name)
        self.assertTrue(nonqueryfound.count() > 0)

    def test_delete_one_by_id(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        row = {"name": name}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        self.app.mongo.deletebyid(table_name=self.table, id=inserted)
        found = self.app.mongo.findbyid(table_name=self.table, id=inserted)
        # Assert
        self.assertEqual(found, None)

    def test_delete_one(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        row = {"name": name}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        self.app.mongo.deleteone(table_name=self.table, query=row)
        found = self.app.mongo.findbyid(table_name=self.table, id=inserted)
        # Assert
        self.assertEqual(found, None)

    def test_delete_many(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        row = {"name": name}
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row=row)
        self.app.mongo.deletemany(table_name=self.table, query=row)
        found = self.app.mongo.findbyid(table_name=self.table, id=inserted)
        # Assert
        self.assertEqual(found, None)

    def test_update_by_id(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        name2 = "UpdatedTestName" + str(uuid.uuid4())
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row={"name": name})
        self.app.mongo.updatebyid(table_name=self.table, id=inserted, newval={"name": name2})
        found = self.app.mongo.findone(table_name=self.table, query={"name": name2})
        # Assert
        self.assertTrue(len(found) > 0)

    def test_update_one(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        name2 = "UpdatedTestName" + str(uuid.uuid4())
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row={"name": name})
        self.app.mongo.updateone(table_name=self.table, query={"name": name}, newval={"name": name2})
        found = self.app.mongo.findone(table_name=self.table, query={"name": name2})
        # Assert
        self.assertTrue(len(found) > 0)

    def test_update_many(self):
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        name2 = "UpdatedTestName" + str(uuid.uuid4())
        # Act
        inserted = self.app.mongo.insert_row(table_name=self.table, row={"name": name})
        self.app.mongo.updatemany(table_name=self.table, query={"name": name}, newval={"name": name2})
        found = self.app.mongo.findone(table_name=self.table, query={"name": name2})
        # Assert
        self.assertTrue(len(found) > 0)

    @classmethod
    def tearDownClass(cls):
        # delete db after tests finished
        cls.app.mongo.client.drop_database(cls.database_name)

    if __name__ == '__main__':
        unittest.main()
