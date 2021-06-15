
# TODO: implement this mock object
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
import cv2
import time
import winsound

class Detector:
    def __init__(self, camId):
        self.camId = camId
        self.activated = False
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        self.eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'harrcasecade_eye_tree_eyeglasses.xml')
        self.cap = None
        self.frame = None # numpy.ndarray

    def start(self) -> None:
        self.activated = True
        self.cap = cv2.VideoCapture(self.camId)

        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture() # FIXME: 이거 어떻게함?

        if not self.cap.isOpened():
            raise IOError('웹캡이 열리지 않았습니다')
        
    
    def stop(self) -> None:
        assert self.activated is True
        if not self.eye_opened():
            self.activated = False
        raise Exception('not Implemented')

    def update(self) -> None:
        assert self.activated is True

        _, self.frame = self.cap.read()

    def get_image(self) -> np.ndarray:
        return self.frame

    def eye_opened(self) -> bool:
        assert self.activated is True # self.activated 가 true 라고 선언 (아닐경우 에러)

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eyeCascade.detectMultiScale(self.gray, 1.1, 4)
        
        return len(eyes) > 0
 
    def eye_closed(self) -> bool:
        assert self.activated is True
    
        return not self.eye_opened()