from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI()
auth_app_url = os.environ.get("AUTH_APP", "localhost")

class UserInput(BaseModel):
    email: str
    password: str

@app.post("/signup")
async def signup(user_input: UserInput):
    email = user_input.email.strip()
    password = user_input.password.strip()

    if not email or not password:
        raise HTTPException(status_code=422, detail="An email and password need to be specified!")

    try:
        # Dummy hashed password and email, replace with actual logic if needed
        # need to change this with sending request auth hashed password
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{auth_app_url}:8003/hashed-password/{password}")

        hashed_pw = response["hashedPassword"]
        print(hashed_pw, email)
        return {"message": "User created!"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/login")
async def login(user_input: UserInput):
    email = user_input.email.strip()
    password = user_input.password.strip()

    if not email or not password:
        raise HTTPException(status_code=422, detail="An email and password need to be specified!")

    # Dummy hashed password and response, replace with actual logic if needed
    # same here we need to send request to token endpoint
    hashed_password = password + "_hash"
    
    async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{auth_app_url}:8003/token/{hashed_password}/{password}")
    # response = {"status": 200, "data": {"token": "abc"}}

    if response["status"] == 200:
        return {"token": response["data"]["token"]}
    else:
        raise HTTPException(status_code=response["status"], detail="Logging in failed!")