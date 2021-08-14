import os
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import cv2
import scipy.ndimage
from inspection.models import EmployeeModel, InspectionModel
from .Rotation import Rotation
from .Image import Image
from .PatternMismatch import PatternMismatch
from .DefectDetection import DefectDetection
import numpy as np
from inspection.gpio import lights
import urllib


class FileStorage(FileSystemStorage):
    def __init__(self, location):
        super().__init__(location)
        self.NEW_PATH = location

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.NEW_PATH, name))
        return name


class Inspection:

    def __init__(self, model_path, inspection_type, inspection_id):
        self.model_path = model_path
        self.inspection_id = inspection_id
        self.inspection_type = inspection_type
        self.host = 'http://127.0.0.1:8000/'
        self.standard_image1 = None
        self.standard_image2 = None

    def saveImage(self, name, image, path):
        ret, buff = cv2.imencode('.jpg', image)
        content = ContentFile(buff.tobytes())
        fs = FileStorage(path)
        fs.save(name, content)

        return str(self.host + path + '/' + name)

    def saveImage_pattern(self, name, image, path):
        ret, buff = cv2.imencode('.jpg', image)
        content = ContentFile(buff.tobytes())
        fs = FileStorage(path)
        fs.save(name, content)
        pathh = os.path.abspath(path + '/' + name)
        return pathh

    def start_inspection(self):
        videocapture = cv2.VideoCapture(1)
        print(videocapture.isOpened())
        _, first_frame = videocapture.read()
        initial_image = Image(first_frame)
        initial_image.cvtGray()
        first_gray = initial_image.blurG((5, 5))

        initial_frame_path = self.saveImage('first_Frame' + str(self.inspection_id) + '.jpg', first_frame,
                                            'media/inspection/{}'.format(self.inspection_id))

        while videocapture.isOpened():
            _, frame_input = videocapture.read()
            frame = Image(frame_input)
            frame_path = self.saveImage(str('Frame' + str(self.inspection_id) + '.jpg'), frame.image,
                                        'media/inspection/{}'.format(self.inspection_id))
            frame.cvtGray()
            gray_frame = frame.blurG((7, 7))
            gray_frame_path = self.saveImage(str('gray_frame' + str(self.inspection_id) + '.jpg'), gray_frame,
                                             'media/inspection/{}'.format(self.inspection_id))
            difference = cv2.absdiff(first_gray, gray_frame)
            _, difference = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)
            cv2.imshow("Difference", difference)
            difference_path = self.saveImage(str('difference' + str(self.inspection_id) + '.jpg'), difference,
                                             'media/inspection/{}'.format(self.inspection_id))

            key = cv2.waitKey(1)
            # esc
            if key == 27:
                break
            elif key == 115:
                # cv2.imwrite("Difference.jpg", difference)
                self.processing(frame_input, difference, frame)

        cv2.destroyAllWindows()
        videocapture.release()

        InspectionModel.objects.filter(id=self.inspection_id).update(initial_frame=initial_frame_path,
                                                                     frame=frame_path,
                                                                     grey_frame=gray_frame_path,
                                                                     difference=difference_path,
                                                                     )

    def processing(self, frame_input, difference, frame):
        median_angle = 0
        lines = None
        img_edges = frame.canny(difference)
        img_edges_b_rotation_path = self.saveImage(str('img_edges_b_rotation' + str(self.inspection_id) + '.jpg'),
                                                   img_edges,
                                                   'media/inspection/{}'.format(self.inspection_id))
        dilation = frame.dilate()
        dilation_b_rotation_path = self.saveImage(str('dilation_b_rotation' + str(self.inspection_id) + '.jpg'),
                                                  dilation,
                                                  'media/inspection/{}'.format(self.inspection_id))
        rotation = Rotation()
        cv2.imshow("img_edges", dilation)

        max_line = rotation.get_max_line(dilation, 50)

        if max_line < 250:
            diff = max_line - 45
        else:
            diff = max_line - 90

        lines = rotation.get_lines(dilation, diff)
        if lines is not None:
            median_angle = rotation.rotation_angle(lines, frame_input)

        rotated_original_image = scipy.ndimage.rotate(frame_input, median_angle, cval=0)
        rotated_original_image_path = self.saveImage(str('rotated_original_image' + str(self.inspection_id) + '.jpg'),
                                                     rotated_original_image,
                                                     'media/inspection/{}'.format(self.inspection_id))
        rotated_binary_image = scipy.ndimage.rotate(difference, median_angle, cval=0)
        cv2.imshow("rotated_original_image", rotated_original_image)
        cv2.waitKey(1)
        img_edges_BINARY = cv2.Canny(rotated_binary_image, 100, 100, apertureSize=3)
        img_edges_a_rotation_path = self.saveImage(str('img_edges_a_rotation' + str(self.inspection_id) + '.jpg'),
                                                   img_edges_BINARY,
                                                   'media/inspection/{}'.format(self.inspection_id))
        contours = frame.findContours(img_edges_BINARY, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            Standard_image2_path = None
            Standard_image2_path = None
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area >= 1500:
                cropped_image = frame.crop_image(rotated_original_image, c)
                cv2.imshow("cropped_image", cropped_image)
                cropped_image_path = self.saveImage(str('cropped_image' + str(self.inspection_id) + '.jpg'),
                                                    cropped_image,
                                                    'media/inspection/{}'.format(self.inspection_id))
                # cv2.imwrite("cropped_image.jpg", cropped_image)
                grey_cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                grey_cropped_image_path = self.saveImage(str('grey_cropped_image' + str(self.inspection_id) + '.jpg'),
                                                         grey_cropped_image,
                                                         'media/inspection/{}'.format(self.inspection_id))
                blur_cropped_image = cv2.GaussianBlur(grey_cropped_image, (7, 7), 0)
                blur_cropped_image_path = self.saveImage(str('blur_cropped_image' + str(self.inspection_id) + '.jpg'),
                                                         blur_cropped_image,
                                                         'media/inspection/{}'.format(self.inspection_id))
                #             grey_cropped_image = cropped.grey_image
                #             blur_cropped_image = cropped.blurred_image
                #             enhanced = cropped.histogram_equalization()

                # enhanced = blur_cropped_image
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(blur_cropped_image)

                enhanced_path = self.saveImage(str('enhanced' + str(self.inspection_id) + '.jpg'),
                                               enhanced,
                                               'media/inspection/{}'.format(self.inspection_id))

                cv2.imshow("original_cropped", enhanced)
                key = cv2.waitKey(0)
                #             Standard (c)
                if key == 99:
                    cv2.imwrite("standard.jpg", cropped_image)
                    Standard_image1_path = self.saveImage_pattern(str('PPM_IM1' + str(self.inspection_id) + '.jpg'),
                                                                  cropped_image,
                                                                  'media/inspection/{}'.format(self.inspection_id))
                    self.standard_image1 = Standard_image1_path
                    standard_image_path = self.saveImage(str('standard_image' + str(self.inspection_id) + '.jpg'),
                                                         cropped_image,
                                                         'media/inspection/{}'.format(self.inspection_id))
                    InspectionModel.objects.filter(id=self.inspection_id).update(standard_image=standard_image_path)

                    print('saved standard image')
                #             Pattern Mismatch (v)
                if key == 118:
                    cv2.imwrite("pattern.jpg", cropped_image)
                    Standard_image2_path = self.saveImage_pattern(str('PPM_IM2' + str(self.inspection_id) + '.jpg'),
                                                                  cropped_image,
                                                                  'media/inspection/{}'.format(self.inspection_id))
                    image_to_compare_path = self.saveImage_pattern(
                        str('image_to_compare' + str(self.inspection_id) + '.jpg'),
                        cropped_image,
                        'media/inspection/{}'.format(self.inspection_id))
                    InspectionModel.objects.filter(id=self.inspection_id).update(image_to_compare=image_to_compare_path,
                                                                                 img_edges_b_rotation=img_edges_b_rotation_path,
                                                                                 dilation_b_rotation=dilation_b_rotation_path,
                                                                                 rotated_image=rotated_original_image_path,
                                                                                 img_edges_a_rotation=img_edges_a_rotation_path,
                                                                                 cropped_image=cropped_image_path,
                                                                                 grey_cropped_image=grey_cropped_image_path,
                                                                                 blurred_cropped_image=blur_cropped_image_path)
                    self.standard_image2 = Standard_image2_path
                    print('saved test image')

                # pattern mismatch (n)
                if key == 110:
                    if self.inspection_type == 'defects_detection':
                        InspectionModel.objects.filter(id=self.inspection_id).update(
                            img_edges_b_rotation=img_edges_b_rotation_path,
                            dilation_b_rotation=dilation_b_rotation_path,
                            rotated_image=rotated_original_image_path,
                            img_edges_a_rotation=img_edges_a_rotation_path,
                            cropped_image=cropped_image_path,
                            grey_cropped_image=grey_cropped_image_path,
                            blurred_cropped_image=blur_cropped_image_path,
                            enhanced_image=enhanced_path)
                        self.defectDetection(enhanced, frame)

                    elif self.inspection_type == 'pattern_mismatch':
                        if self.standard_image1 is not None and self.standard_image2 is not None:

                            self.patternMismatch(self.standard_image1, self.standard_image2)

                        else:
                            print("Give missing Image")



        else:
            median_angle = 0
            lines = None

        cv2.destroyAllWindows()

    def defectDetection(self, enhanced, frame):
        label = []
        lables = ""
        defectRatio = {}
        crack = 0
        pinhole = 0
        spot = 0
        uniq = []
        count = []
        defectRatio = {}
        countvar = 0
        new = 0


        defects = DefectDetection(self.model_path, enhanced)
        thresholded_crop, dilation = defects.enhancement((3, 3))
        thresholded_crop_path = self.saveImage(str('binary_cropped' + str(self.inspection_id) + '.jpg'),
                                               thresholded_crop,
                                               'media/inspection/{}'.format(self.inspection_id))
        cv2.imshow('binary_cropped', thresholded_crop)
        originalunique, originalcounts = np.unique(thresholded_crop, return_counts=True)

        morphed_cropped = self.saveImage(str('morphed_cropped' + str(self.inspection_id) + '.jpg'),
                                         dilation,
                                         'media/inspection/{}'.format(self.inspection_id))
        cv2.imshow('morphed_cropped', dilation)
        cropped_contours = frame.findContours(dilation, cv2.CHAIN_APPROX_SIMPLE)
        for region in cropped_contours:
            area = cv2.contourArea(region)
            if area >= 30:
                (xa, ya, wa, ha) = cv2.boundingRect(region)
                test_image = dilation[ya:(ya + ha), xa:(xa + wa)]
                Testuniq, TestCount = (np.unique(test_image, return_counts=True))
                print("test image", Testuniq, TestCount)
                countvar = originalcounts[1] - TestCount[1]
                new = originalcounts[0] + countvar
                trial= ((TestCount[1] / new) * 100)

                str_trial=str(round(trial,2))
                label = defects.predict_image(test_image)

                if label[0] == 'spot':
                    if area <= 100 and area >= 1:
                        #
                        pinhole += 1
                        labels = "pinhole" + str(pinhole)+" "+str_trial+"%"

                        cv2.putText(enhanced, labels, (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                    else:
                        spot += 1
                        labels = "spot" + str(spot)+" "+str_trial+"%"
                        cv2.putText(enhanced, labels, (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
                else:
                    crack += 1
                    labels = "crack" + str(crack)+" "+str_trial+"%"
                    cv2.putText(enhanced, labels, (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
                defectRatio[labels] = ((TestCount[1] / new) * 100)
                # if label == 'spot':
                #     if area <= 90:
                #         cv2.putText(enhanced, 'pinhole', (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
                #     else:
                #         cv2.putText(enhanced, label, (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
                #     cv2.rectangle(enhanced, (xa, ya), (xa + wa, ya + ha), (0, 0, 255), 2)
                # else:
                #     cv2.putText(enhanced, label, (xa, ya - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
                #     cv2.rectangle(enhanced, (xa, ya), (xa + wa, ya + ha), (0, 0, 255), 2)
        cv2.imshow("Result", enhanced)
        result_path = self.saveImage(str('Output' + str(self.inspection_id) + '.jpg'),
                                     enhanced,
                                     'media/inspection/{}'.format(self.inspection_id))
        # countvar = originalcounts[1] - TestCount[1]
        # new = originalcounts[0] + countvar
        # defectRatio[labels] = ((TestCount[1] / new) * 100)

        cv2.waitKey(0)

        InspectionModel.objects.filter(id=self.inspection_id).update(binary_cropped=thresholded_crop_path,
                                                                     morphed_cropped=morphed_cropped,
                                                                     defected_image=result_path)
        print("defect ratio", defectRatio)

    def patternMismatch(self, imageA, imageB):
        pmm = PatternMismatch(imageA, imageB)
        pmm.resizeImages((480, 480))
        pmm.grayImages()
        diff = pmm.subtractImages()
        cv2.imshow("difference", diff)
        cv2.waitKey(1)
        thresh = 60
        binary, opening = pmm.binaryImage(thresh, (3, 3))
        thresholded_crop_path = self.saveImage(str('binary' + str(self.inspection_id) + '.jpg'),
                                               binary,
                                               'media/inspection/{}'.format(self.inspection_id))
        morphed_cropped = self.saveImage(str('morphed_cropped' + str(self.inspection_id) + '.jpg'),
                                         opening,
                                         'media/inspection/{}'.format(self.inspection_id))
        cnts = pmm.findContours(opening.copy())
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(pmm.resizedA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(pmm.resizedB, (x, y), (x + w, y + h), (0, 0, 255), 2)

        result_path_final = self.saveImage(str('Result_final' + str(self.inspection_id) + '.jpg'),
                                           pmm.resizedB,
                                           'media/inspection/{}'.format(self.inspection_id))
        cv2.imshow("Original", pmm.resizedA)
        cv2.imshow("Modified", pmm.resizedB)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", opening)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        InspectionModel.objects.filter(id=self.inspection_id).update(binary_cropped=thresholded_crop_path,

                                                                     morphed_cropped=morphed_cropped,

                                                                     defected_image=result_path_final)
