

from fastapi import APIRouter, File, Form, UploadFile
from pydantic import BaseModel
from controllers.upload_service import PhotoUploadService

router = APIRouter()


@router.post("/uploadSingleImage")
def uploadSingleImage(
        folder: str = Form(...),
        image: UploadFile = File(...)
    ):
    PhotoUploadService.process(folder, image)