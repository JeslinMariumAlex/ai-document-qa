# database.py
import os
from dotenv import load_dotenv
# sqlalchemy is a SQL Object Relational Mapper (ORM) for Python.
# create_engine is a function that creates a new SQLAlchemy Engine instance, which is the starting point for any SQLAlchemy application.
from sqlalchemy import create_engine
# sessionmaker is used to create new SQLAlchemy Session objects, which are used to interact with the database.
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
# tells python where our postgresQL database is located.
DATABASE_URL = os.getenv("DATABASE_URL")

# engine is sQLalchemys connection interface to database.
engine = create_engine(DATABASE_URL)

# A session is what we will use to perform database operation such as creating , reading and updating documents.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This is the base class we will use for defining our database models.
Base = declarative_base()