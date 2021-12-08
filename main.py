from typing import Match
import cv2
import numpy as np
import time 
from datetime import datetime
flag_move_detection = False



resolution_index = 1
resolutions =[(480, 240), (640, 480), (1280, 720)]
ltime = []
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # 0 -> index of camera
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

video_recorder =None
old_img = None


def change_brightness(val):
    cam.set(cv2.CAP_PROP_BRIGHTNESS, val)

def change_contrast(val):
    cam.set(cv2.CAP_PROP_CONTRAST, val)

def change_resolution():
    global resolution_index
    resolution_index = (resolution_index+1) % len(resolutions)
    cam.set(3, resolutions[resolution_index][0])
    cam.set(4, resolutions[resolution_index][1])

def move_detection(img):
        global old_img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if old_img is None:
            old_img = gray
            return
            
        diff_frame = cv2.absdiff(old_img, gray)
            
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            
          
        cnts,_ = cv2.findContours(thresh_frame.copy(),
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
           
           
        for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                #  making green rectangle around the moving object
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            
        cv2.imshow("movmenet frame", gray)
def print_screen(img):
    print("saving to file")
    cv2.imwrite("filename.jpg",img)


cv2.namedWindow("cam-test")
cv2.createTrackbar("Brightness", "cam-test", int(cam.get(cv2.CAP_PROP_BRIGHTNESS)), 255, change_brightness)
cv2.createTrackbar("Contrast", "cam-test", int(cam.get(cv2.CAP_PROP_CONTRAST)), 255, change_contrast)
while True:
    s, img = cam.read()
    if s:    # frame captured without any errors
        
   
        
        # record frame 
        if video_recorder :
             video_recorder.write(img)
        
        
     
        key_input= cv2.waitKey(10) 
        # turn off a window 
        if key_input == 27:
            break
        # make screenshot on clicking 
        if key_input == ord('1'):
            print_screen(img)
        # record image 
        if key_input == ord('2'):
            
            if video_recorder:
                print("Stop Recording")
                video_recorder.release()
                video_recorder = None
            else:
                print("Recording ")
                video_recorder = cv2.VideoWriter("output.avi", fourcc, 20, resolutions[resolution_index])
        # change picture resolution 
        if key_input == ord('3') and not flag_move_detection and not video_recorder:
            change_resolution()
            
        if key_input == ord('4'):
            flag_move_detection = not flag_move_detection
           
        if flag_move_detection:
            move_detection(img)
     
        
        
        cv2.imshow("cam-test",img)


cam.set(cv2.CAP_PROP_BRIGHTNESS, 128)     
cam.set(cv2.CAP_PROP_CONTRAST, 32)
cam.release()

cv2.destroyAllWindows()
