from sqlalchemy.orm import Session

import models, utils, schemas

from snowflake import SnowflakeGenerator

idgen = SnowflakeGenerator(42)

# get user data

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_fullname(db: Session, realname: str):
    return db.query(models.User).filter(models.User.realname == realname).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# create user data

def create_user(db: Session, user):
    hashed_password = utils.hash_pwd(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, id=next(idgen), username=user.username, realname=user.realname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_forum(db: Session, forum):
    db_forum = models.Forum(title=forum.title, id=next(idgen), banner_url = forum.banner_url)
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum

def get_forum(db: Session, forum_id: int):
    return db.query(models.Forum).filter(models.Forum.id == forum_id).first()

def get_forum_by_name(db: Session, forum_name: str):
    return db.query(models.Forum).filter(models.Forum.name == forum_name).first()

def create_topic(db: Session, topic):
    db_topic = models.Topic(name=topic.name, id=next(idgen), topic_id=next(idgen))
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topic_by_name(db: Session, topic_name: str):
    return db.query(models.Topic).filter(models.Topic.name == topic_name).first()

def get_posts_for_topic(db: Session, topic_id: int):
    return db.query(models.Post).filter(models.Post.id == topic_id).first()