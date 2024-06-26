import os
import face_recognition
from numpy import ndarray
import shutil

class FaceProcessor:

    basePath = 'assets/'
    encodingNumber = 0
    """
    TODO: clean up file paths (pass this in from main class/variable when running script??)
    TODO: add some more validation checking on the face. Play around with thresholds in the compare_faces() function
    Other papers for future reference:
    https://github.com/davidsandberg/facenet    https://pypi.org/project/keras-facenet/
    https://arxiv.org/abs/1503.03832
    https://github.com/cmusatyalab/openface
    """

    def __init__(self, basePath):
        self.basePath = basePath

    def faceSegmentation(self):
        self.albumPath = self.basePath
        print(f"Conducting face segmentation and analysis for photos in the folder: {self.albumPath}")
        albumPhotosFullPath = os.listdir(self.albumPath)

        allEncodings = self.getAllFaceEncodings(albumPhotosFullPath)

        organisedEncodings = {}

        while allEncodings:
            currEncodingName, (currEncoding, currPhotoPath) = allEncodings.popitem()
            organisedEncodings[currEncodingName] = [(currEncoding, currPhotoPath)]

            allEncodingsValues = list(allEncodings.values())

            for encoding, photoPath in allEncodingsValues:
                result = face_recognition.compare_faces([currEncoding], encoding, 0.45)
                if result[0]:
                    organisedEncodings[currEncodingName].append((encoding, photoPath))

        self.loggingToTerminal(organisedEncodings)
        self.makeDirectories(organisedEncodings)
        return

    def loggingToTerminal(self, organisedEncodings):
        print(f'Found {len(organisedEncodings)} faces.')
        for face, listOfData in organisedEncodings.items():
            print(f'Found {face} in {len(listOfData)} photos.')
        return

    def makeDirectories(self, organisedEncodings):
        newAlbumPath = self.albumPath+"_face_organised"
        if not os.path.exists(newAlbumPath):
            print(f"Creating folder for organised images by face at: {newAlbumPath}")
            os.makedirs(newAlbumPath)
        
        for face, listOfData in organisedEncodings.items():
            newFacePath = newAlbumPath+"/"+face
            if not os.path.exists(newFacePath):
                print(f"Creating folder for new face at: {newFacePath}")
                os.makedirs(newFacePath)
            for _, photoPath in listOfData:
                shutil.copy(photoPath, newFacePath)
        return

    def getAllFaceEncodings(self, albumPhotosFullPath: list[str]) -> dict:
        allEncodings = {}

        for photoName in albumPhotosFullPath:
            if not photoName.startswith('.'):
                photoPath = self.albumPath+'/'+photoName
                loadedImage = face_recognition.load_image_file(photoPath)
                photoEncodings:list[ndarray] = face_recognition.face_encodings(loadedImage)
                for encoding in photoEncodings:
                    encodingName = 'encoding'+str(self.encodingNumber)
                    allEncodings[encodingName] = (encoding, photoPath)
                    self.encodingNumber += 1

        return allEncodings