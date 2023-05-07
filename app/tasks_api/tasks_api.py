import os
import json
from fastapi import FastAPI, HTTPException, Header, Request
from typing import Optional
import httpx
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()
auth_app_url = os.environ.get("AUTH_APP", "localhost")

TASKS_FOLDER = os.environ.get("TASKS_FOLDER", "tasks")
file_path = Path(TASKS_FOLDER, "tasks.txt")
file_path.parent.mkdir(parents=True, exist_ok=True)

class Task(BaseModel):
    title: str
    text: str

async def extract_and_verify_token(headers):
    if "authorization" not in headers:
        raise HTTPException(status_code=401, detail="No token provided.")
    token = headers["authorization"].split(" ")[1]  # expects Bearer TOKEN

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{auth_app_url}:8003/verify-token/{token}")

    if response.status_code == 200:

        return response.json()["uid"]
    else:
        raise HTTPException(status_code=401, detail="Failed to verify token.")

@app.get("/tasks")
async def get_tasks(request: Request):
    try:
        uid = await extract_and_verify_token(request.headers)  # we don't really need the uid
        with file_path.open("r") as f:
            data = f.read()
        entries = data.split("TASK_SPLIT")
        entries.pop()  # remove last, empty entry
        tasks = [json.loads(json_task) for json_task in entries]
        return {"message": "Tasks loaded.", "tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/tasks")
async def create_task(task: Task, authorization: Optional[str] = Header(None)):
    try:
        headers = {"authorization": authorization}
        uid = await extract_and_verify_token(headers)  # we don't really need the uid
        json_task = json.dumps(task.dict())
        with file_path.open("a") as f:
            f.write(json_task + "TASK_SPLIT")
        return {"message": "Task stored.", "createdTask": task}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not verify token.")