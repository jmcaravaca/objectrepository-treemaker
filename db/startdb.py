from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import UIObject, Activity, Base
from secret import DBCONNSTRING


# Create a SQLAlchemy engine and session
engine = create_engine(DBCONNSTRING)
Session = sessionmaker(bind=engine)
session = Session()


# Create the table in the database (only needed once)
def create_db(eng=engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db(engine)
