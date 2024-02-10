import shutil
import cv2
import os
import numpy as np

from src.literalProperties.duplicateProcessor import DuplicateProcessor
from src.literalProperties.exposureProcessor import ExposureProcessor
from src.literalProperties.faceProcessor import FaceProcessor

class LiteralProcessor:

    basePath = 'assets/'

    def __init__(self, albumPath):
        self.basePathAlbum = self.basePath + albumPath
        self.faceProcessor = FaceProcessor()
        self.duplicateProcessor = DuplicateProcessor(self.basePathAlbum)
        self.exposureProcessor = ExposureProcessor(self.basePathAlbum)
        
    def processAlbum(self):
        """ 
        TODO: add some ordering / interconnectivity between functionalities 
        to prevent unecessary duplication of images
        """
        self.duplicateProcessor.duplicateGrouping()
        self.blurrinessSeparation(40)
        self.faceProcessor.faceSegmentation('photoAlbum1')
        self.exposureProcessor.exposureSeparation()
        
    def blurrinessSeparation(self, threshold):
        allImagesPaths = os.listdir(self.basePathAlbum)
        blurryImages = []
        nonBlurryImages = []
        for imagePath in allImagesPaths:
            if not imagePath.startswith('.'): # dont include hidden files
                image = cv2.imread(self.basePathAlbum+'/'+imagePath)
                _, blurrinessScore, _ = self.calcBlurriness(image)
                if blurrinessScore < threshold:
                    blurryImages.append(imagePath)
                else:
                    nonBlurryImages.append(imagePath)
        
        print(f"Found {len(blurryImages)} blurry images, {len(nonBlurryImages)} non-blurry images. Creating two separate folders.")
        self.createFoldersBlurriness(blurryImages, nonBlurryImages)
    
    def createFoldersBlurriness(self, blurryImages, nonBlurryImages):
        blurryImagesPath = self.basePathAlbum+'_blurry'
        notBlurryImagesPath = self.basePathAlbum+'_notBlurry'
        self.createFolder(blurryImagesPath)
        self.createFolder(notBlurryImagesPath)

        for imageName in blurryImages:
            oldPhotoPath = self.basePathAlbum+"/"+imageName
            shutil.copy(oldPhotoPath, blurryImagesPath)

        for imageName in nonBlurryImages:
            oldPhotoPath = self.basePathAlbum+"/"+imageName
            shutil.copy(oldPhotoPath, notBlurryImagesPath)

        print(f"Folders for blurry images created at {blurryImagesPath} and {notBlurryImagesPath}")

    
    def createFolder(self, path):
        if not os.path.exists(path):
            print(f"Creating folder for duplicate groupings at: {path}")
            os.makedirs(path)

    def calcBlurriness(self, image: np.ndarray):
        """
        https://github.com/WillBrennan/BlurDetection2
        https://github.com/isalirezag/HiFST ?
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_map = cv2.Laplacian(image, cv2.CV_64F)
        score = np.var(blur_map)

        return blur_map, score, bool(score<20)
