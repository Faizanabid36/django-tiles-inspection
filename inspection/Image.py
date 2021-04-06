import cv2
import numpy as np
import imutils


class Image:
    def __init__(self, image):
        self.image = image
        self.first_frame = image
        self.gray = None
        self.blurred = None
        self.edged = None
        self.dilated = None
        self.cropped_image = None

    def cvtGray(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self.gray

    def blurG(self, kernel=(5, 5)):
        self.blurred = cv2.GaussianBlur(self.gray, kernel, 0)
        return self.blurred

    def canny(self, image):
        self.edged = cv2.Canny(image, 100, 100, apertureSize=3)
        return self.edged

    def dilate(self, kernel=np.ones((5, 5), np.uint8), iterations=1):
        self.dilated = cv2.dilate(self.edged, kernel, iterations)
        return self.dilated

    def findContours(self, image, algo):
        contours = cv2.findContours(image, cv2.RETR_EXTERNAL, algo)
        return imutils.grab_contours(contours)

    def crop_image(self, image, points):
        (x, y, w, h) = cv2.boundingRect(points)
        self.cropped_image = image[y + 10:(y + h) - 10, x + 10:(x + w) - 10]
        return self.cropped_image


