
import os
from fastapi import File, UploadFile

class PhotoUploadService:

    def __init__(self) -> None:
        pass

    def process(
            folderName: str,
            image: UploadFile = File(...)
        ):
        if not os.path.exists(f"/Users/udaiarneja/Github/ai_photography/assets/{folderName}"):
            print(f"Creating folder for duplicate groupings at: /Users/udaiarneja/Github/ai_photography/assets/{folderName}")
            os.makedirs(f"/Users/udaiarneja/Github/ai_photography/assets/{folderName}")
        try:
            with open(f"/Users/udaiarneja/Github/ai_photography/assets/{folderName}/{image.filename}", "wb+") as file_object:
                file_object.write(image.file.read())
        except Exception as error:
            print(error)
            print("error")