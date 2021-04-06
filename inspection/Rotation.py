import cv2
import numpy as np
import math


class Rotation:
    def get_lines(self, img, minLineLength):
        return cv2.HoughLinesP(img, 1, math.pi / 180.0, 100, minLineLength=minLineLength, maxLineGap=10)

    def get_max_line(self, img, minLineLength=50):
        val = []
        all_lines = self.get_lines(img, 50)
        if all_lines is not None:
            for [[x1, y1, x2, y2]] in all_lines:
                val.append(math.sqrt(pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2)))
        if len(val) > 0:
            return max(val)
        return 180

    def rotation_angle(self, lines, frame):
        angles = []
        for [[x1, y1, x2, y2]] in lines:
            frame_copy = frame.copy()
            cv2.line(frame_copy, (x1, y1), (x2, y2), (255, 0, 0), 3)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)
        return np.median(angles)
