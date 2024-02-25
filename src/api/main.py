from fastapi import FastAPI

app = FastAPI()

import controllers.login as login
import controllers.upload as upload

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login.router)
app.include_router(upload.router)