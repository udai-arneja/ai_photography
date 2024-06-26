from fastapi import FastAPI

app = FastAPI()

import api.controllers.login as login
import api.controllers.upload as upload
import api.controllers.download as download
import api.controllers.process as process

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login.router)
app.include_router(upload.router)
app.include_router(download.router)
app.include_router(process.router)