from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# https://fastapi.tiangolo.com/tutorial/sql-databases/

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	affilation = Column(String, primary_key=True, index=True, nullable=True) # allows sorting by school
	email = Column(String, unique=True, index=True)
	username = Column(String, unique=True, index=True)
	realname = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True)

class Topic(Base):
	__tablename__ = "topics"

	id = Column(Integer, primary_key=True, index=True)

class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, index=True)

class Forum(Base):
	__tablename__ = "forums"

	id = Column(Integer, primary_key=True, index=True)

