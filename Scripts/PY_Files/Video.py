import cv2
import pyvirtualcam as pyvircam

class Video():
    
    def __init__(self):
        self.w = cv2.CAP_PROP_FRAME_WIDTH
        self.h = cv2.CAP_PROP_FRAME_HEIGHT
        self.fps = cv2.CAP_PROP_FPS
        self.cam = cv2.VideoCapture(0)
        self.fmt = pyvircam.PixelFormat.BGR
    
    def CheckCamValid(self):
        isValid,frm = self.cam.read()
        self.cam.release()
        return isValid