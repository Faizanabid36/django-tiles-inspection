import cv2
import numpy as np
from .Image import Image
from .PredictionModel import ModelDetector


class DefectDetection:
    def __init__(self, model_path, image):
        model = ModelDetector(model_path)
        model.loadFile()
        self.model = model
        im = Image(image)
        self.image = im.image
        self.binary_crop = None

    def enhancement(self, kernel):
        thresholded_crop = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                 11, 2)
        self.binary_crop = thresholded_crop
        kernel_dilate = np.ones(kernel, np.uint8)
        # dilation = cv2.dilate(thresholded_crop, kernel_dilate, iterations=1)
        dilation = cv2.morphologyEx(thresholded_crop, cv2.MORPH_OPEN, kernel)
        return thresholded_crop, dilation

    def predict_image(self, image):
        return self.model.predict_image(image)
