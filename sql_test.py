import unittest, uuid
from api import create_app
from database.sql.models import Test
from database.sql import db_drop_all
from sqlalchemy_utils import drop_database


# python -m unittest discover -p sql_test.py

class SQLDBTestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = str(uuid.uuid4())[:8]
        cls.app = create_app(test_database="test_" + cls.session)
        cls.database_name = "test_" + cls.session
        cls.table = "ttest_" + cls.session
        print(cls.database_name)

    # -----------------------------------------------------------test cases ------------------------------------------------------------
    def test_insert_row(self):
        print("1")
        # Arrange
        test = Test(title="Test that!" + str(uuid.uuid4())[:8])
        # Act
        test.insert()
        # Assert
        self.assertTrue(test.id)

    def test_findbyid(self):
        print("2")
        # Arrange
        test = Test(title="Test that!" + str(uuid.uuid4())[:8])
        # Act
        test.insert()
        found = Test.query.filter_by(id=test.id).first()
        # Assert
        self.assertTrue(test.id)
        self.assertEqual(test.id, found.id)

    def test_findone(self):
        print("3")
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        test = Test(title=name)
        # Act
        test.insert()
        found = Test.query.filter_by(title=name).first()
        # Assert
        self.assertTrue(test.id)
        self.assertEqual(found.title, test.title)

    def test_find(self):
        print("4")
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        test = Test(title=name)
        # Act
        test.insert()
        found = Test.query.filter_by(title=name).all()
        # Assert
        self.assertTrue(test.id)
        self.assertTrue(len(found) > 0)

    def test_delete(self):
        print("5")
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        test = Test(title=name)
        # Act
        test.insert()
        test.delete()
        found = Test.query.filter_by(title=name).all()
        found2 = Test.query.filter_by(id=test.id).all()
        # Assert
        self.assertTrue(len(found) == 0)
        self.assertTrue(len(found2) == 0)

    def test_update_one(self):
        print("6")
        # Arrange
        name = "TestName" + str(uuid.uuid4())
        test = Test(title=name)

        # Act
        test.insert()
        name2 = "TestName" + str(uuid.uuid4())
        test.title = name2
        test.update()
        found = Test.query.filter_by(id=test.id).first()

        # Assert
        self.assertEqual(found.title, name2)

    @classmethod
    def tearDownClass(cls):
        # delete db after tests finished
        db_drop_all(testing=True, conn=cls.app.config["SQLALCHEMY_DATABASE_URI"])

    if __name__ == '__main__':
        unittest.main()
