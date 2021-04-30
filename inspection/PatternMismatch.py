import cv2
import numpy as np
import imutils
from .Image import Image
from .Preprocessing import PreprocessedImage


class PatternMismatch:
    def __init__(self, imageA, imageB):
        im1 = Image(cv2.imread(imageA))
        im2 = Image(cv2.imread(imageB))
        self.imageA = im1.image
        self.imageB = im2.image
        self.resizedA = None
        self.resizedB = None
        self.grayA = None
        self.grayB = None
        self.diff = None
        self.opening = None

    def resizeImages(self, dim):
        pp = PreprocessedImage(self.imageA)
        pp1 = PreprocessedImage(self.imageB)
        self.resizedA = pp.resize(dim)
        self.resizedB = pp1.resize(dim)

    def grayImages(self):
        self.grayA = cv2.cvtColor(self.resizedA, cv2.COLOR_BGR2GRAY)
        self.grayB = cv2.cvtColor(self.resizedB, cv2.COLOR_BGR2GRAY)

    def subtractImages(self):
        self.diff = cv2.subtract(self.grayA, self.grayB)
        return self.diff

    def binaryImage(self, thresh_val, kernel):
        print('thres',int(self.diff.max()))
        thresh = cv2.threshold(self.diff, thresh_val, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones(kernel, np.uint8)
        # self.opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        self.dilate = cv2.dilate(thresh, kernel, iterations=1)
        return thresh, self.dilate

    def findContours(self, image):
        contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return imutils.grab_contours(contours)
