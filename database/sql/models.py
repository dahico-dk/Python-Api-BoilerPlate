from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine

db = SQLAlchemy()


class ModelBase():
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        # properties must be changed before calling this method
        db.session.commit()


class Test(db.Model, ModelBase):
    def __init__(self, title):
        self.title = title

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
