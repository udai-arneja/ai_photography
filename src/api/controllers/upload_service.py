
from fastapi import File, UploadFile


class PhotoUploadService:

    def __init__(self) -> None:
        pass

    def process(
            file_loc: str,
            my_file: UploadFile = File(...)
        ):
        try:
            with open(f"/Users/udaiarneja/Github/ai_photography/assets/{file_loc}", "wb+") as file_object:
                file_object.write(my_file.file.read())
        except Exception as error:
            print(error)
            print("error")