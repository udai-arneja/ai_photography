import base64
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
        firstImageLocation = location+"/"+os.listdir(location)[0]
        image_data_base64 = ""
        with open(firstImageLocation, "rb") as image_file:
            image_data_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        return {
            "name": albumName,
            "created": readableTime,
            "quanImages": noOfImages,
            "profileImageEncoded": image_data_base64
        }

    def getPhotosFromAlbum(self, user: str, albumName:str):
        albumLocation = self.currLoc+user+"/"+albumName
        imageEncodings = []
        for image in os.listdir(albumLocation):
            image = albumLocation+"/"+image
            image_data_base64 = ""
            with open(image, "rb") as image_file:
                image_data_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            imageEncodings.append(image_data_base64)
        return imageEncodings
