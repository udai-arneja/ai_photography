from datetime import datetime
import os

class PhotoDownloadService:

    currLoc = "/Users/udaiarneja/Github/ai_photography/assets/"

    def __init__(self) -> None:
        pass

    def getUserAlbums(self, user: str) -> dict:
        albumData = []
        directories = os.listdir(self.currLoc + user)

        for albumName in directories:
            if(albumName[0] != "."):
                location = self.currLoc + user + "/" + albumName
                albumData.append(self.createAlbumData(albumName, location))

        return {
            "albumData": albumData,
            "metaData": []
        }

    def createAlbumData(self, albumName, location):
        creationTime = os.stat(location).st_birthtime
        readableTime = datetime.utcfromtimestamp(creationTime).strftime('%Y-%m-%d %H:%M:%S')

        noOfImages = len(os.listdir(location))
        return {
            "name": albumName,
            "created": readableTime,
            "quanImages":noOfImages
        }
