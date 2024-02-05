import cv2

def duplicateGroupingHashing(self, albumName, threshold):
    # TODO: if subject/photo is the same but has been slightly moved then image gives diff hash
    # need to see how much by & what other hashings may be better
    path = self.basePath+albumName
    albumPhotosFullPath = os.listdir(path)
    
    albumPhotosHash = {}

    for photo in albumPhotosFullPath:
        photoPath = path+'/'+photo
        hsh = cv2.img_hash.BlockMeanHash_create()
        photoHash = hsh.compute(cv2.imread(photoPath))
        integerHashValue = int.from_bytes(photoHash.tobytes(), byteorder='big', signed=False)
        albumPhotosHash[integerHashValue] = (photoPath)

    return albumPhotosHash