from imageProcess.literalProperties.processor import LiteralProcessor

LiteralProcessor

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
        self.literalProcessor = LiteralProcessor('photoAlbum1')
        None

    def literalProperties(self):
        self.literalProcessor.processAlbum()

    def semanticProperties():
        None