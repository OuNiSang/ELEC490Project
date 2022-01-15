from os import stat
from sre_parse import State
import cv2 ## for the webcam and computer vision
import sys
import numpy as np 
import face_recognition ## face recognition
import matplotlib.pyplot as plt
import pyvirtualcam as vircam
import time

from playsound import playsound ## alert sound
from PIL import Image, ImageDraw
from tensorflow import keras ## for loading in the model

dir_Detection = './DetectionSource/'

class Detection():
    
    def __init__(self):
        self.eye_model = keras.models.load_model(dir_Detection +    '80best.h5')
        self.lip_model = keras.models.load_model(dir_Detection +    '80lip_best.h5')
        self.eye = 0
        self.lip = 0
        self.i = 0
                

        
    def DetectByFrame(self, frame):
        # initiate
        w = 1024
        h = 768
        self.i += 1

        # set a counter
        
        counter = 0

        while True:
            t_start = time.time()
            frame_count = 0
            if frame_count == 0:
                frame_count += 1
                pass
            else:
                count = 0
                continue

            # function called on the frame
            image_for_prediction = self.eye_cropper(frame)
            image_for_prediction_lip = self.lip_cropper(frame)
            t_2 = time.time()
            try:
                image_for_prediction = np.array(image_for_prediction)
                image_for_prediction = np.expand_dims(image_for_prediction, axis=0)
                image_for_prediction_lip = np.array(image_for_prediction_lip)
                image_for_prediction_lip = np.expand_dims(image_for_prediction_lip, axis=0)
                # get prediction from model
                prediction = self.eye_model.predict(image_for_prediction)
                prediction_lip = self.lip_model.predict(image_for_prediction_lip)
                prediction = np.argmax(prediction[0], axis=0)
                prediction_lip = np.argmax(prediction_lip[0], axis=0)
            except:
                continue
            t_3 = time.time()
            
            #print(prediction_lip)
            t_4 = time.time()
            if prediction == 1:
                self.eye += 1
            else: 
                self.eye = 0
            if prediction_lip == 1:
                self.lip += 1
            else: 
                self.lip = 0
            # Based on prediction, display either "Open Eyes" or "Closed Eyes"

            if self.lip <2 and self.eye < 5:
                counter = 0
                status = 'No_Yawn + Eye_Open'

                #cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)

                cv2.putText(frame, status, (round(w/2)-80,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_4)
                x1, y1,w1,h1 = 0,0,175,75
                ## Draw black backgroun rectangle
                cv2.rectangle(frame, (x1,x1), (x1+w1-20, y1+h1-20), (0,0,0), -1)
                ## Add text
                cv2.putText(frame, 'Active', (x1 +int(w1/10), y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,0),2)
    
            elif self.lip > 2 and self.eye > 5:
                counter = counter + 1
                status = 'Yawn + Eye_closed'

                #cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)

                cv2.putText(frame, status, (round(w/2)-104,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_4)
                x1, y1,w1,h1 = 0,0,175,75
                ## Draw black backgroun rectangle
                cv2.rectangle(frame, (x1,x1), (x1+w1-20, y1+h1-20), (0,0,0), -1)
                ## Add text
                cv2.putText(frame, 'Active', (x1 +int(w1/10), y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,0),2)

            elif self.lip < 2 and self.eye > 5:
                counter = counter + 1
                status = 'No_Yawn + Eye_closed'

                #cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)

                cv2.putText(frame, status, (round(w/2)-104,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_4)
                x1, y1,w1,h1 = 0,0,175,75
                ## Draw black backgroun rectangle
                cv2.rectangle(frame, (x1,x1), (x1+w1-20, y1+h1-20), (0,0,0), -1)
                ## Add text
                cv2.putText(frame, 'Active', (x1 +int(w1/10), y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,0),2)

                # if the counter is greater than 3, play and show alert that user is asleep
            else: 
                counter = counter + 1
                status = 'Yawn + Eye_Open'

                #cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)

                cv2.putText(frame, status, (round(w/2)-104,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_4)
                x1, y1,w1,h1 = 0,0,175,75
                ## Draw black backgroun rectangle
                cv2.rectangle(frame, (x1,x1), (x1+w1-20, y1+h1-20), (0,0,0), -1)
                ## Add text
                cv2.putText(frame, 'Active', (x1 +int(w1/10), y1+int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,0),2)
            t_5 = time.time()
            if counter > 2:

                x1, y1, w1, h1 = 400,400,400,100

                cv2.rectangle(frame, (round(w/2) - 160, round(h) - 200), (round(w/2) + 160, round(h) - 120), (0,0,255), -1)

                cv2.putText(frame, 'SLEEPING', (round(w/2)-136,round(h) - 146), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_4)

                cv2.imshow('Drowsiness Detection', frame)
                k = cv2.waitKey(1)
                ## Sound
                #playsound('rooster.mov')
                counter = 1
                continue
            t_6 = time.time()
            t_crop = t_2 - t_start
            t_predictRdy = t_3 - t_2
            t_predict = t_4 - t_3
            t_classify = t_5 - t_4
            # print('\r'+"Crop: {0}\t PredicRdy: {1}\t Predict: {2}\t Classify: {3}\t In Status: {4}".format(t_crop, t_predictRdy, t_predict, t_classify, status) ,end=' ')
            print('\r'+"lip:{0}\t eye:{1}\t status:{2}\t".format(self.lip, self.eye, status), end=' ')
            return frame    
        
    def lip_cropper(self, frame):
        facial_features_list = face_recognition.face_landmarks(frame)
        lips = []
        try:
            lips.append(facial_features_list[0]['top_lip'])
            lips.append(facial_features_list[0]['bottom_lip'])
        except:
            return

        x_max1 = max([coordinate[0] for coordinate in lips[0]])
        y_max1 = max([coordinate[1] for coordinate in lips[0]])
        x_min2 = min([coordinate[0] for coordinate in lips[1]])
        y_min2 = min([coordinate[1] for coordinate in lips[1]])
        x_range = x_max1 - x_min2
        y_range = y_max1 - y_min2
        #print(lips[1])
        #print(lips)
        #print(x_max1,x_min1,y_max1,y_min1)
        #print(x_range,y_range)

        if x_range > y_range:
            right = int(round(.3*x_range) + x_max1)
            left = int(x_min2 - round(.3*x_range))
            bottom = int(round(((right-left) - y_range))/2 + y_max1)
            top = int(y_min2 - round(((right-left) - y_range))/2)
        else:
            bottom = int(round(.3*y_range) + y_max1)
            top = int(y_min2 - round(.3*y_range))
            right = int(round(((bottom-top) - x_range))/2 + x_max1)
            left = int(x_min2 - round(((bottom-top) - x_range))/2)

        #print(bottom,top,right,left)
        cropped = frame[top:(bottom + 1), left:(right + 1)]
        # resize the image

        #cropped = cv2.resize(cropped, (32,32))
        #image_for_prediction = cropped.reshape(-1, 32, 32, 3)
        image_for_prediction = cv2.resize(cropped, (80,80))


        return image_for_prediction
    
    def eye_cropper(self, frame):

        # create a variable for the facial feature coordinates

        facial_features_list = face_recognition.face_landmarks(frame)


        # create a placeholder list for the eye coordinates
        # and append coordinates for eyes to list unless eyes
        # weren't found by facial recognition

        try:
            eye = facial_features_list[0]['left_eye']
        except:
            try:
                eye = facial_features_list[0]['right_eye']
            except:
                return


        # establish the max x and y coordinates of the eye

        x_max = max([coordinate[0] for coordinate in eye])
        x_min = min([coordinate[0] for coordinate in eye])
        y_max = max([coordinate[1] for coordinate in eye])
        y_min = min([coordinate[1] for coordinate in eye])


        # establish the range of x and y coordinates

        x_range = x_max - x_min
        y_range = y_max - y_min


        # in order to make sure the full eye is captured,
        # calculate the coordinates of a square that has a
        # 50% cushion added to the axis with a larger range and
        # then match the smaller range to the cushioned larger range

        if x_range > y_range:
            right = round(.5*x_range) + x_max
            left = x_min - round(.5*x_range)
            bottom = round((((right-left) - y_range))/2) + y_max
            top = y_min - round((((right-left) - y_range))/2)
        else:
            bottom = round(.5*y_range) + y_max
            top = y_min - round(.5*y_range)
            right = round((((bottom-top) - x_range))/2) + x_max
            left = x_min - round((((bottom-top) - x_range))/2)


        # crop the image according to the coordinates determined above

        cropped = frame[top:(bottom + 1), left:(right + 1)]

        # resize the image

        #cropped = cv2.resize(cropped, (32,32))
        #image_for_prediction = cropped.reshape(-1, 32, 32, 3)
        image_for_prediction = cv2.resize(cropped, (80,80))


        return image_for_prediction
