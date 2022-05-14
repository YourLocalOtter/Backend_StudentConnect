from typing import Union, List
# let's get the database from the other file
from . import crud, models, schemas
from .database import SessionLocal, engine

# if database doesn't exist then make them
models.Base.metadata.create_all(bind=engine)

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

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
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

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
	return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	if limit > 100:
		# why in the world would you want to look at more than 100 users at a time
		raise HTTPException(status_code=400, detail="Limit exceeds reasonable maximum.")
	users = crud.get_users(db, skip=skip, limit=limit)
	return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id=user_id)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user

def main():
	# Run!
	print("Not supposed to run it this way")

if __name__ == '__main__':
	main()