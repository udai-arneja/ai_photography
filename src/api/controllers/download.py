from fastapi import APIRouter

from api.service.download import PhotoDownloadService


router = APIRouter()

@router.get("/getUserAlbum")
def getUserAlbums(
        user: str,
    ):
    return PhotoDownloadService().getUserAlbums(user)