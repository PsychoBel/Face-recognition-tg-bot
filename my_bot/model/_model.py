import numpy as np
import imutils
import cv2
import dlib
from os.path import join, dirname


class FullModel():
    def __init__(self):
        '''Initialize weights of model'''
        directory = join(dirname(__file__), 'tmp_weights')
        MEAN_VALUE_1 = 78.4263377603
        MEAN_VALUE_2 = 87.7689143744
        MEAN_VALUE_3 = 114.895847746
        self.MODEL_MEAN_VALUES = (MEAN_VALUE_1, MEAN_VALUE_2, MEAN_VALUE_3)
        self.age_list = ['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
        self.gender_list = ['Male', 'Female']
        
        self.net = cv2.dnn.readNetFromCaffe(f"{directory}/deploy.prototxt", f"{directory}/res10_300x300_ssd_iter_140000.caffemodel")
        self.age_net = cv2.dnn.readNetFromCaffe(
                                f"{directory}/deploy_age.prototxt",
                                f"{directory}/age_net.caffemodel")
        self.gender_net = cv2.dnn.readNetFromCaffe(
                                f"{directory}/deploy_gender.prototxt",
                                f"{directory}/gender_net.caffemodel")
        
    def predict(self, frame):
        '''Function for prediction gender and age'''
        src_hight, src_width = frame.shape[:2]
        dst_width = 300
        frame = imutils.resize(frame, width=dst_width)
        factor = src_width / dst_width
        dst_hight = src_hight / factor

        detector = dlib.get_frontal_face_detector()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        det_input = frame.transpose(2, 0, 1)
        det_input = det_input.reshape(1, *det_input.shape)
        self.net.setInput(det_input)
        rects = self.net.forward()
        rects = rects.reshape(*rects.shape[2:])[:, 2:]
        new_rects = []
        genders = []
        ages = []

        for rect in rects:
            if rect[0] < 0.9:
                continue
            else:
                rect = rect[1:]
            x1, y1, x2, y2 = rect
            x1, y1, x2, y2 = int(x1 * dst_width), int(y1 * dst_hight), int(x2 * dst_width), int(y2 * dst_hight)

            a = 0.1
            aw = a * (x2 - x1)
            ah = a * (y2 - y1)
            x1, x2, y1, y2 = np.array([x1 - aw, x2 + aw, y1 - ah, y2 + ah]).astype(int)
            
            new_rects.append(np.array([x1, y1, x2, y2]) * factor)
            
            face_img = frame[y1:y2, x1:x2].copy()

            blob2 = cv2.dnn.blobFromImage(face_img, 1, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
            self.gender_net.setInput(blob2)
            gender_preds = self.gender_net.forward()
            gender = self.gender_list[gender_preds[0].argmax()]
            genders.append(gender)

            self.age_net.setInput(blob2)
            age_preds = self.age_net.forward()
            age = self.age_list[age_preds[0].argmax()]
            ages.append(age)
        return new_rects, genders, ages


def transform(frame, rects, genders, ages):
    '''Function for transform picture'''
    frame = frame.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for rect, gender, age in zip(rects, genders, ages):
        x1, y1, x2, y2 = rect.astype(int)
        overlay_text = "{}, {}".format(gender, age)
        cv2.putText(frame, overlay_text ,(x1, y1), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame