from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/verify-token/{token}")
def verify_token(token: str):
    print(f"Toke Received {token}")
    if token == "abc":
        return {"message": "Valid token.", "uid": "u1"}
    else:
        raise HTTPException(status_code=401, detail="Token invalid.")

@app.get("/token/{hashed_password}/{entered_password}")
def get_token(hashed_password: str, entered_password: str):
    if hashed_password == entered_password + "_hash":
        token = "abc"
        return {"message": "Token created.", "data": {"token": token}}
    else:
        raise HTTPException(status_code=401, detail="Passwords do not match.")

@app.get("/hashed-password/{password}")
def get_hashed_password(password: str):
    hashed_password = password + "_hash"
    return {"hashedPassword": hashed_password}