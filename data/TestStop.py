import numpy as np
import cv2

path = 'cascade.xml'
stop_cascade = cv2.CascadeClassifier(path)


from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

while 1:
    img = cv2.imread('testimage.jpg')
    print('hello')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    stop = stop_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in stop:
        print('nigga')
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Stop Sign',(x-w,y-h), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
        cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
