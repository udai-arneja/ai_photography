import shutil
from imagededup.methods import CNN
import os

class DuplicateProcessor:

    cnn_encoding = CNN()

    def __init__(self, basePathAlbum) -> None:
        self.basePathAlbum = basePathAlbum
    
    def duplicateGrouping(self):
        # could merge with hashing approach so there is a reduced cross matching required (cnn more costly than hashing)
        print(self.basePathAlbum)
        duplicated_PhotosDict = self.cnn_encoding.find_duplicates(image_dir=self.basePathAlbum, min_similarity_threshold=0.80, scores=False)
        groupedPhotos = self.groupDuplicatedPhotos(duplicated_PhotosDict)
        self.createFolders(groupedPhotos)
        return duplicated_PhotosDict
    
    def groupDuplicatedPhotos(self, imagesDict: dict[str, list[str]]):
        allGroups = []
        while imagesDict:
            image, listOfImages = imagesDict.popitem()
            currentSet = set({image})
            while listOfImages:
                currImage = listOfImages.pop(0)
                if not currImage in currentSet:
                    listOfImages += imagesDict[currImage]
                    imagesDict.pop(currImage)
                    currentSet.add(currImage)
            allGroups.append(currentSet)
        return allGroups
    
    def createFolders(self, groupedPhotos: list[set[str]]):
        duplicateFoldersPath = self.basePathAlbum+'_duplicates'
        self.createFolder(duplicateFoldersPath)

        groupNumber = 0
        for imagesSet in groupedPhotos:
            duplicateGroupPath = duplicateFoldersPath+"/"+str(groupNumber)
            if not os.path.exists(duplicateGroupPath):
                print(f"Creating folder for new duplicate group {groupNumber} at: {duplicateGroupPath}")
                os.makedirs(duplicateGroupPath)
            for imageName in imagesSet:
                oldPhotoPath = self.basePathAlbum+"/"+imageName
                shutil.copy(oldPhotoPath, duplicateGroupPath)
            groupNumber+=1

    def createFolder(self, path):
        if not os.path.exists(path):
            print(f"Creating folder for duplicate groupings at: {path}")
            os.makedirs(path)