import shutil
import cv2
import numpy as np
import os
from imagededup.methods import CNN

from src.literalProperties.faceProcessor import FaceProcessor

class LiteralProcessor:

    imageToProcess = None
    basePath = 'assets/'
    cnn_encoding = CNN()

    def __init__(self, albumPath):
        self.faceProcessor = FaceProcessor()
        self.basePathAlbum = self.basePath + albumPath
        
    def processAlbum(self):
        # group photos based on duplicates
        self.duplicateGrouping()

        # identify blurry images and separate
        self.blurrinessSeparation(40)

        # self.faceProcessor.faceSegmentation('photoAlbum1')
        # print(self.duplicateGroupingHashing('photoAlbum1', 0))
        # print("Exposure/Histogram Values: "+str(self.exposureValue()))
        # print("Blurriness Value: "+str(self.blurrinessValue()))
    
    def duplicateGrouping(self):
        # could merge with hashing approach so there is a reduced cross matching required (cnn more costly than hashing)
        duplicated_PhotosDict = self.cnn_encoding.find_duplicates(image_dir=self.basePathAlbum, min_similarity_threshold=0.80, scores=False)
        groupedPhotos = self.groupDuplicatedPhotos(duplicated_PhotosDict)
        self.createFolders(groupedPhotos)
        return duplicated_PhotosDict
        
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

    def calcBlurriness(self, image: np.ndarray):
        """
        https://github.com/WillBrennan/BlurDetection2
        https://github.com/isalirezag/HiFST ?
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_map = cv2.Laplacian(image, cv2.CV_64F)
        score = np.var(blur_map)

        return blur_map, score, bool(score<20)

    def exposureValue(self): # -1, 0, 1 -> under, normal, over
        # TODO: add thresholding logic, initial version relative to spikes in histogram?
        bgr_planes = cv2.split(self.imageToProcess)
        histSize = 256
        histRange = (0, 256)
        b_hist = cv2.calcHist(bgr_planes, [0], None, [histSize], histRange, accumulate=False)
        g_hist = cv2.calcHist(bgr_planes, [1], None, [histSize], histRange, accumulate=False)
        r_hist = cv2.calcHist(bgr_planes, [2], None, [histSize], histRange, accumulate=False)

        hist_w = 512
        hist_h = 400
        bin_w = int(round( hist_w/histSize ))
        histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

        cv2.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
        for i in range(1, histSize):
            cv2.line(histImage, ( bin_w*(i-1), hist_h - int(b_hist[i-1]) ),
                    ( bin_w*(i), hist_h - int(b_hist[i]) ),
                    ( 255, 0, 0), thickness=2)
            cv2.line(histImage, ( bin_w*(i-1), hist_h - int(g_hist[i-1]) ),
                    ( bin_w*(i), hist_h - int(g_hist[i]) ),
                    ( 0, 255, 0), thickness=2)
            cv2.line(histImage, ( bin_w*(i-1), hist_h - int(r_hist[i-1]) ),
                    ( bin_w*(i), hist_h - int(r_hist[i]) ),
                    ( 0, 0, 255), thickness=2)
        cv2.imshow('Source image', self.imageToProcess)
        cv2.imshow('calcHist Demo', histImage)
        # cv2.waitKey()

        # TODO: get top 5/10, bottom 5/10 average. subtract max value from photo. if remainder is greater than 0 then over/under exposed => return  -1, +1
        """ TODO: papers/githubs => check how it determines whether/what to change in the photo
                https://github.com/mahmoudnafifi/Deep_White_Balance  
                https://github.com/mahmoudnafifi/Exposure_Correction  https://arxiv.org/pdf/2003.11596.pdf
                https://github.com/hmshreyas7/low-light-detection
        """
        
        return -1

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
