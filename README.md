# Connect with Students
## Developers!
You will need to install the following modules `fastapi`,`sqlalchemy` (database), and `snowflake-id` (which generates unique ids for everyone).
```
pip install fastapi sqlalchemy snowflake-id
```
Next we'll install something to make JWT session tokens (you don't need to understand this).
```
pip install python-jose[cryptography] 
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