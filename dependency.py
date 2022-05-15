import config

from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
security = HTTPBearer()

async def check_access(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, key = config.SECRET, algorithms=[config.ALGORITHM])
        return payload["uid"]
    except JOSEError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))


