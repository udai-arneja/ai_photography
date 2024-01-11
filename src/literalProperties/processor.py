
class LiteralProcessor:

    imageToProcess = None

    def __init__(self, image):
        self.imageToProcess = image
    
    def process(self):
        print("Found image with dimensions: ", self.imageToProcess.shape, " . Processing.")
        

    
