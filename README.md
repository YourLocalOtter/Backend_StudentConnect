# Connect with Students
## Developers!
You will need to install the following modules `fastapi` and `sqlalchemy`.
```
pip install fastapi sqlalchemy
```
For testing you also need a "ASGI server" which I don't know what it stands for. Here's a command for installing uvicorn.
```
pip install "uvicorn[standard]"
```
We can now run the app with
```
uvicorn main:app --reload --port 8888
```
(hopefully you've got everything setup properly)