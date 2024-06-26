import json
from fastapi import APIRouter, Response

from api.service.download import PhotoDownloadService

router = APIRouter()

@router.get("/getUserAlbum")
def getUserAlbums(
        user: str,
    ):
    albumsInfo = PhotoDownloadService().getUserAlbums(user)
    response_content = json.dumps(albumsInfo)
    # highly inefficent, try to use StreamingResponse
    return Response(content=response_content, media_type="application/json")

@router.get("/getPhotosFromAlbum")
def get_items_from_album(user: str, albumName: str, ):
    albumsInfo = PhotoDownloadService().getPhotosFromAlbum(user, albumName)
    response_content = json.dumps(albumsInfo)
    # highly inefficent, try to use StreamingResponse
    return Response(content=response_content, media_type="application/json")