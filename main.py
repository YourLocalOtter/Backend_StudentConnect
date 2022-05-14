from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/accounts/{uid}")
def get_account(uid: int, full: Union[bool, None] = None):
    # return {"uid": uid, "full": full}
	if not uid:
		return {"message": "Missing uid"}

def main():
	# Run!
	print("Not supposed to run it this way")

if __name__ == '__main__':
	main()