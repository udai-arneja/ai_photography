from fastapi import APIRouter

from imageProcess.photoProcessor import PhotoProcessor

router = APIRouter()

@router.get("/processAlbum")
def processAlbum():
    PhotoProcessor().literalProperties()
    return {}