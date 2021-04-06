import cv2


class PreprocessedImage:
    def __init__(self, image):
        self.image = image
        self.grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.blurred_image = cv2.GaussianBlur(self.grey_image, (3, 3), 0)
        self.enhanced_image = None

    def resize(self, dim=(480, 480)):
        return cv2.resize(self.image, dim)

    def adaptive_histogram_equalization(self):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.enhanced_image = clahe.apply(self.grey_image)
        return self.enhanced_image

    # def histogram_equalization(self):
    #     self.enhanced_image = cv2.equalizeHist(self.grey_image)
    #     return self.enhanced_image
