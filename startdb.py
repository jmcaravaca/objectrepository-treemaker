from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UIObject, Activity, Base


def CreateDB(eng):
    Base.metadata.create_all(engine)

# Create a SQLAlchemy engine and session
engine = create_engine('sqlite:///uidata.db')
Session = sessionmaker(bind=engine)
session = Session()
# Create the table in the database (only needed once)

if __name__ == '__main__':
    CreateDB(engine)