import cv2
import numpy as np
import os

class LiteralProcessor:

    imageToProcess = None

    def __init__(self, image):
        self.imageToProcess = image
    
    def process(self):
        print("Found image with dimensions: ", self.imageToProcess.shape, ". Processing.")
        print(self.duplicateGrouping('photoAlbum1', 0))
        print("Exposure/Histogram Values: "+str(self.exposureValue()))
        print("Blurriness Value: "+str(self.blurrinessValue()))

    def duplicateGrouping(self, albumName, threshold):
        # TODO: if subject/photo is the same but has been slightly moved then image gives diff hash
        # need to see how much by & what other hashings may be better
        basePath = 'assets/'+albumName
        albumPhotosFullPath = os.listdir(basePath)
        
        albumPhotosHash = {}

        for photo in albumPhotosFullPath:
            photoPath = basePath+'/'+photo
            hsh = cv2.img_hash.BlockMeanHash_create()
            photoHash = hsh.compute(cv2.imread(photoPath))
            integerHashValue = int.from_bytes(photoHash.tobytes(), byteorder='big', signed=False)
            albumPhotosHash[integerHashValue] = (photoPath)

        return albumPhotosHash

    def blurrinessValue(self):
       return cv2.Laplacian(self.imageToProcess, cv2.CV_64F).var()

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
        return -1

