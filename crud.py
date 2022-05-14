from sqlalchemy.orm import Session

import models, utils, schemas

from snowflake import SnowflakeGenerator

idgen = SnowflakeGenerator(42)

# get user data

def get_uer(db: Session, user_id: int):
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