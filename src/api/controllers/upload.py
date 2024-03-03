

from fastapi import APIRouter, File, Form, UploadFile
from api.service.upload_service import PhotoUploadService

router = APIRouter()


@router.post("/uploadSingleImage")
def uploadSingleImage(
        folder: str = Form(...),
        image: UploadFile = File(...)
    ):
    PhotoUploadService.process(folder, image)