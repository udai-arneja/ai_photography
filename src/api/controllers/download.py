from fastapi import APIRouter

from api.service.download import PhotoDownloadService


router = APIRouter()

@router.post("/getUserAlbum")
def uploadSingleImage(
        user: str,
    ):
    return PhotoDownloadService().getUserAlbums(user)