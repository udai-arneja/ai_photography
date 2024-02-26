

from fastapi import APIRouter, File, UploadFile
from controllers.upload_service import PhotoUploadService

router = APIRouter()

@router.post("/uploadSingleImage")
def uploadSingleImage(
        # destination: str,
        my_file: UploadFile = File(...)
        ):
    PhotoUploadService.process(my_file.filename,my_file)
    print(my_file.file)
    print()
    return