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
	realname = Column(String, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True)

class Topic(Base):
	__tablename__ = "topics"

	id = Column(Integer, primary_key=True, index=True)

	topic_id = Column(Integer, ForeignKey("forums.id"))
	topic = relationship("Forum", back_populates="topics")

	who_started_id = Column(Integer, ForeignKey("users.id"))
	who_started = relationship("User", back_populates="users")

	title = Column(String(128))

class Post(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, index=True)

	topic_id = Column(Integer, ForeignKey("topics.id"))
	topic = relationship("Topic", back_populates="posts")

	poster = relationship("User", back_populates="users")
	poster_id = Column(Integer)

	content = Column(String(128))

class Forum(Base):
	__tablename__ = "forums"

	id = Column(Integer, primary_key=True, index=True)
	desc = Column(String(2048))
	name = Column(String(128))
	banner_url = Column(String(512))