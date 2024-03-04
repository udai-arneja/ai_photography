
import os
from fastapi import File, UploadFile

class PhotoUploadService:

    def __init__(self) -> None:
        pass

    def process(
            userName: str,
            folderName: str,
            image: UploadFile = File(...)
        ):
        print(folderName)
        if not os.path.exists(f"/Users/udaiarneja/Github/ai_photography/assets/{userName}/{folderName}"):
            print(f"Creating folder for duplicate groupings at: /Users/udaiarneja/Github/ai_photography/assets/{userName}/{folderName}")
            os.makedirs(f"/Users/udaiarneja/Github/ai_photography/assets/{userName}/{folderName}")
        try:
            with open(f"/Users/udaiarneja/Github/ai_photography/assets/{userName}/{folderName}/{image.filename}", "wb+") as file_object:
                file_object.write(image.file.read())
        except Exception as error:
            print(error)
            print("error")