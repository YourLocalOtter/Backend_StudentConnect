from typing import Union, List
# let's get the database from the other file
import crud, models, schemas, utils, dependency
from database import SessionLocal, engine

# if database doesn't exist then make them
models.Base.metadata.create_all(bind=engine)

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from jose import jwt

import config

app = FastAPI()

# CORS, allows the frontend to talk to the backend. by default browsers will block this otherwise some random sketchy website could instruct your bank to do stuff

origins = [
	"http://localhost",
	"http://localhost:3000",
	"http://localhost:5000",
	"http://localhost:8080"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins, # using all for now cause whitelist causes bugs
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# nasty workaround for cors not getting set on error
# sourced from
# https://github.com/tiangolo/fastapi/issues/775#issuecomment-592946834
async def catch_exceptions_middleware(request: Request, call_next):
	try:
		return await call_next(request)
	except Exception as ex:
		print("Server Error!",ex)
		return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

# uh I believe this make sures we actually have a database when someone makes a request
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.get("/")
def read_root():
	return {"Hello": "World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	if not user.email or not "@" in user.email: # check if it is actually a email
		raise HTTPException(status_code=400, detail="Invalid email")
	return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	if limit > 100:
		# why in the world would you want to look at more than 100 users at a time
		raise HTTPException(status_code=400, detail="Limit exceeds reasonable maximum.")
	users = crud.get_users(db, skip=skip, limit=limit)
	return users

import datetime

@app.post("/users/authenticate")
def authenticate_a_user(user_req: schemas.UserAuthenticateReq, db: Session = Depends(get_db)):
	# check if the user exists
	db_user = crud.get_user_by_email(db, email=user_req.email)
	if db_user is None:
		raise HTTPException(status_code=400, detail="Invalid email or password")
	# check if the password is correct
	if not utils.check_pwd(user_req.password, db_user.hashed_password):
		raise HTTPException(status_code=400, detail="Invalid email or password")
	# if it passes all the tests, return the user

	return jwt.encode({"uid": db_user.id,"exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},key = config.SECRET)

@app.get("/users/me", response_model = schemas.UserPrivate)
def read_current_user(uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id = uid)
	if db_user is None:
		raise HTTPException(status_code = 404, detail="User not found")
	return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id=user_id)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user

@app.get("/forums/{forum_id}", response_model = schemas.Forum)
def get_a_forum(forum_id: int,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_forum = crud.get_forum(db, forum_id = forum_id)
	if db_forum is None:
		raise HTTPException(status_code = 404, detail="Forum not found")
	return db_forum

@app.get("/forums_by_name/{forum_name}", response_model = schemas.Forum)
def get_a_forum_by_name(forum_name: str,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_forum = crud.get_forum_by_name(db, forum_name = forum_name)
	if db_forum is None:
		raise HTTPException(status_code = 404, detail="Forum not found")
	return db_forum

@app.post("/forums", response_model = schemas.Forum)
def make_a_forum(forum: schemas.ForumBase,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_forum = crud.create_forum(forum)
	return db_forum

@app.get("/topics/{topic_id}", response_model = schemas.Topic)
def get_a_topic(topic_id: int,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_topic = crud.get_topic(db, topic_id = topic_id)
	if db_topic is None:
		raise HTTPException(status_code = 404, detail="Topic not found")
	return db_topic

@app.get("/topics_by_name/{topic_name}", response_model = schemas.Topic)
def get_a_topic_by_name(topic_name: str,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_topic = crud.get_topic_by_name(db, topic_name = topic_name)
	if db_topic is None:
		raise HTTPException(status_code = 404, detail="Topic not found")
	return db_topic

@app.post("/topics", response_model = schemas.Topic)
def make_a_topic(topic: schemas.TopicBase,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_topic = crud.create_topic(db, topic, uid)
	return db_topic

@app.get("/posts", response_model = schemas.Post)
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	if limit > 100:
		# why in the world would you want to look at more than 100 posts at a time
		raise HTTPException(status_code=400, detail="Limit exceeds reasonable maximum.")
	posts = crud.get_posts(db, skip=skip, limit=limit)
	return posts

@app.post("/posts", response_model = schemas.Post)
def make_a_post(post: schemas.PostBase,uid: int = Depends(dependency.check_access),db: Session = Depends(get_db)):
	db_post = crud.create_post(db, post, uid)
	return db_post

def main():
	# Run!
	print("Not supposed to run it this way")

if __name__ == '__main__':
	main()