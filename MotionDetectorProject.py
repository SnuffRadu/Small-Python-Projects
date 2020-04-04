import numpy as np
from cv2 import cv2
import pandas
import time
import datetime


def motiondetector():

    cap = cv2.VideoCapture(0)
    first_frame = None

    while (True):

        # Captura cadru cu cadru
        ret, frame = cap.read()

        status = 0

        #se intampla chestii aici
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0)

        if first_frame is None:
            first_frame = grayscale
            continue

        delta_frame = cv2.absdiff(first_frame, grayscale)
        threshold_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        threshold_delta = cv2.dilate(threshold_delta, None, iterations = 4)

        # verifica versiunea de opencv
        major = cv2.__version__.split('.')[0]
        if major == '3':
            ret, contours, hierarchy = cv2.findContours(threshold_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(threshold_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                status = 1
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if status == 1:
            time = datetime.datetime.now()
            print(time)

        # Display the resulting frame
        cv2.imshow('frame', grayscale)
        cv2.imshow('delta', delta_frame)
        cv2.imshow('thresh', threshold_delta)
        cv2.imshow('frame', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

motiondetector()