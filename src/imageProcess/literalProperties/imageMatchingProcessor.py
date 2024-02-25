import cv2

# not effective, to be improved
class ImageMatchingProcessor:

    """"
    SuperGlue github matching
    ./match_pairs.py --resize 1600 --superglue outdoor --max_keypoints 2048 --nms_radius 3  --resize_float --input_dir assets/photoAlbum1/ --output_dir dump_match_pairs_outdoor --viz --input_pairs assets/test.txt --keypoint_threshold 0.5 --match_threshold 0.2
    """

    def __init__(self, basePathAlbum) -> None:
        self.basePathAlbum = basePathAlbum
        self.orb = cv2.ORB_create() 
        self.matcher = cv2.BFMatcher() 

    def imageMatching(self):
        keypoints1, descriptors1 = self.getImageDescriptors(self.basePathAlbum+'/'+'DSC_0292.JPG')
        image1 = cv2.imread(self.basePathAlbum+'/'+'DSC_0292.JPG')
        keypoints2, descriptors2 = self.getImageDescriptors(self.basePathAlbum+'/'+'DSC_0291.JPG')
        image2 = cv2.imread(self.basePathAlbum+'/'+'DSC_0291.JPG')
        matches = self.matcher.match(descriptors1, descriptors2)
        final_img = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:20],None)
        print(len(matches))
        cv2.imshow("Matches", final_img)
        cv2.waitKey()
    
    def getImageDescriptors(self, imagePath):
        print(imagePath)
        image = cv2.imread(imagePath)
        # TODO: add error handling
        imageBW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keyPoints, descriptors = self.orb.detectAndCompute(imageBW,None) 
        return (keyPoints, descriptors)
    
    
