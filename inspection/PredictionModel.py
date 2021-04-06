from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy
import cv2
import os
import glob
import _pickle as cPickle


class PredictionModel:
    def rescale(self, image, scale_percent=60):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        return dim

    def image_vector(self, image, size=(128, 128)):
        return cv2.resize(image, size).flatten()

    def image_to_predict(self, test_image):
        defeccted_region = []
        vector_image = self.image_vector(test_image)
        defeccted_region.append(vector_image)
        return numpy.array(defeccted_region)


class ModelTrainer(PredictionModel):

    def __init__(self, path):
        self.path = path
        self.imagemaxtrix = []
        self.imagelabels = []
        self.modelSVM = None

    def read_dataset(self):
        return list(glob.glob(self.path))

    def build_matrix(self):
        imagePaths = self.read_dataset()
        for (i, path) in enumerate(imagePaths):
            # load the image and extract the class label
            image = cv2.imread(path, 0)
            label = path.split(os.path.sep)[-1].split(".")[0]
            pm = PredictionModel()
            pixels = pm.image_vector(image)
            # update the images and labels matricies respectively
            self.imagemaxtrix.append(pixels)
            self.imagelabels.append(label)

        self.imagemaxtrix = numpy.array(self.imagemaxtrix)
        self.imagelabels = numpy.array(self.imagelabels)

    def train_model(self, kernel='linear'):
        (train_img, test_img, train_label, test_label) = train_test_split(
            self.imagemaxtrix, self.imagelabels, test_size=0.1, random_state=50)
        self.modelSVM = SVC(max_iter=-1, kernel=kernel, class_weight='balanced', gamma='scale')
        self.modelSVM.fit(train_img, train_label)
        accuracy = self.modelSVM.score(test_img, test_label)
        print("SVM model accuracy: {:.2f}%".format(accuracy * 100))
        f = open("svm.cpickle", "wb")
        f.write(cPickle.dumps(self.modelSVM))
        f.close()

    def predict_image(self, test_image):
        image = PredictionModel.image_to_predict(test_image)
        label = self.modelSVM.predict(image)
        return label[0]


class ModelDetector(PredictionModel):
    def __init__(self, path):
        self.path = path
        self.model = None

    def loadFile(self):
        with open(self.path, 'rb') as f:
            self.model = cPickle.load(f)

    def predict_image(self, image):
        test_model = PredictionModel()
        predictable = test_model.image_to_predict(image)
        label = self.model.predict(predictable)
        return label[0]
