import uvicorn
from multiprocessing import Process

from auth_api.auth_api import app as auth_app
from tasks_api.tasks_api import app as tasks_app
from users_api.users_api import app as users_app

def run_auth_app():
    uvicorn.run(auth_app, host="localhost", port=8003)

def run_tasks_app():
    uvicorn.run(tasks_app, host="localhost", port=8001)

def run_users_app():
    uvicorn.run(users_app, host="localhost", port=8002)

if __name__ == "__main__":
    auth_process = Process(target=run_auth_app)
    tasks_process = Process(target=run_tasks_app)
    users_process = Process(target=run_users_app)

    auth_process.start()
    tasks_process.start()
    users_process.start()

    auth_process.join()
    tasks_process.join()
    users_process.join()