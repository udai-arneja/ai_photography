from src.literalProperties.processor import LiteralProcessor
import cv2

class PhotoProcessor:

    """
    Base class for processing images.

    Consisting of 
        1. literal properties - blurriness, brightness, duplications
        2. semantic properties
    """

    imageToProcess = None
    literalProcessor = None

    def __init__(self) -> None:
        self.loadImages()
        self.literalProcessor = LiteralProcessor('photoAlbum1')
        None

    def literalProperties(self):
        self.literalProcessor.processAlbum()

    def semanticProperties():
        None
    
    def loadImages(self):
        path = 'assets/photoAlbum1/IMG_6979.JPG'
        print('Loading image')
        self.imageToProcess = cv2.imread(path)
        print('Image loaded.')
