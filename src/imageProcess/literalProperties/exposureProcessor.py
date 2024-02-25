

import os
import shutil
import cv2
from matplotlib import pyplot as plt
import numpy as np


""" TODO: papers/githubs => check how it determines whether/what to change in the photo
        https://github.com/mahmoudnafifi/Deep_White_Balance  
        https://github.com/mahmoudnafifi/Exposure_Correction  https://arxiv.org/pdf/2003.11596.pdf
        https://github.com/hmshreyas7/low-light-detection
"""

""""TODO: 
    add face segmentation => produce a mask => push mask through hist image to check exposure quality
    https://pyimagesearch.com/2021/01/19/image-masking-with-opencv/
    (could this also be applied to blur processing?)
"""

class ExposureProcessor:

    def __init__(self, basePathAlbum) -> None:
        self.basePathAlbum = basePathAlbum

    def exposureSeparation(self):
        allImagesPaths = os.listdir(self.basePathAlbum)
        poorExposureImagePaths = []
        undeterminedExposureImagePaths = []
        goodExposureImagePaths = []

        for imagePath in allImagesPaths:
            if not imagePath.startswith('.'):
                image = cv2.imread(self.basePathAlbum+'/'+imagePath)
                exposureRatio = self.exposureTest(image)
                if exposureRatio < 0.4:
                    poorExposureImagePaths.append(imagePath)
                elif exposureRatio < 1:
                    undeterminedExposureImagePaths.append(imagePath)
                else:
                    goodExposureImagePaths.append(imagePath)

        self.createFolders(poorExposureImagePaths, '_poorExposure')
        self.createFolders(undeterminedExposureImagePaths, '_undeterminedExposure')
        self.createFolders(goodExposureImagePaths, '_goodExposure')

    
    def exposureTest(self, image:np.ndarray):
        histSize = 512
        section = 20
        histogramChannels = self.getHistChannels(image, histSize)

        overallMaxRatio = 0
        for histogramChannel in histogramChannels:
            flattenedHistVals = [histVal for histValList in histogramChannel for histVal in histValList]
            maxUpper = max(flattenedHistVals[0:section])
            maxLower = max(flattenedHistVals[len(flattenedHistVals)-section:])
            maxImage = max(flattenedHistVals[section:len(flattenedHistVals)-section])
            if maxLower != 0 and maxUpper != 0:
                currMaxRatio = max((maxImage/maxLower), (maxImage/maxUpper))
                overallMaxRatio = max(overallMaxRatio, currMaxRatio)

        # self.viewImages(overallMaxRatio, histogramChannel, image)
    
        return overallMaxRatio
    
    def getHistChannels(self, image:np.ndarray, histSize:int) -> list[list[list[int]]]:
        histogramChannels = []
        histogramChannels.append(cv2.calcHist([image], [0], None, [histSize], (0,256)))
        histogramChannels.append(cv2.calcHist([image], [1], None, [histSize], (0,256)))
        histogramChannels.append(cv2.calcHist([image], [2], None, [histSize], (0,256)))
        return histogramChannels
    
    def createFolders(self, imagePaths:list[str], folderNameExt:str):
        newFolderFullPath = self.basePathAlbum+folderNameExt
        self.createFolder(newFolderFullPath)
        for imagePath in imagePaths:
            if not imagePath.startswith('.'):
                oldPhotoPath = self.basePathAlbum+"/"+imagePath
                shutil.copy(oldPhotoPath, newFolderFullPath)
        return
    
    def createFolder(self, path):
        if not os.path.exists(path):
            print(f"Creating folder for duplicate groupings at: {path}")
            os.makedirs(path)
    
    def viewImages(self, overallMaxRatio, histogramChannel, image):
        print(overallMaxRatio)
        fig, axs = plt.subplots(2)
        axs[0].plot(histogramChannel)
        axs[1].imshow(image)
        fig.show()
        fig.waitforbuttonpress()
