from datetime import datetime
import os

class PhotoDownloadService:

    def __init__(self) -> None:
        pass

    def getUserAlbums(self, user: str) -> dict:
        albumData = []
        currLoc = "/Users/udaiarneja/Github/ai_photography/assets/"
        directories = os.listdir(currLoc + user)

        for albumName in directories:
            location = currLoc + user + "/" + albumName
            creationTime = os.stat(location).st_birthtime
            albumData.append(self.createAlbumData(albumName, creationTime))

        return {
            "albumData": albumData,
            "metaData": []
        }

    def createAlbumData(self, albumName, createdTime):
        readableTime = datetime.utcfromtimestamp(createdTime).strftime('%Y-%m-%d %H:%M:%S')
        return {
            "name": albumName,
            "created": readableTime
        }
