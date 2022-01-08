import cv2
import pyvirtualcam as pyvircam

class Video():
    
    def __init__(self):
        self.w = cv2.CAP_PROP_FRAME_WIDTH
        self.h = cv2.CAP_PROP_FRAME_HEIGHT
        self.fps = cv2.CAP_PROP_FPS
    
    def CheckCamValid(self):
        try:
            with pyvircam.Camera(width=self.w, height=self.h, fps=self.fps) as cam:
                print("Video Camera Valid Check Pass")
        except:
            print("ERROR, Check your Camera setting")