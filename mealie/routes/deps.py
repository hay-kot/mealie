from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from mealie.core.config import SECRET
from mealie.db.database import db
from mealie.db.db_setup import create_session, generate_session
from mealie.schema.auth import Token, TokenData
from mealie.schema.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
ALGORITHM = "HS256"


async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(generate_session)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print("Login Payload", token_data)
    except JWTError:
        raise credentials_exception
    user = db.users.get(session, token_data.username, "email")
    if user is None:
        raise credentials_exception
    return user



