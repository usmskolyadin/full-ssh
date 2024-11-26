from datetime import timedelta
from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, Form, Cookie, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.schemas.auth import SUser
from server.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, hash_password, fake_users_db, verify_password

router = APIRouter()

@router.post("/register/")
async def register(username: str = Form(...), password: str = Form(...)):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    fake_users_db[username] = SUser(username=username, hashed_password=hash_password(password), email="", full_name="")
    return {"message": "User registered successfully!"}

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    response = Response(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    
    return response

# Выход пользователя
@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully!"}

# Защищенный маршрут
@router.get("/users/me/")
async def read_users_me(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user