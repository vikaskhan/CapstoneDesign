import numpy as np
import cv2

path = 'cascade.xml'
stop_cascade = cv2.CascadeClassifier(path)


from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


img = cv2.imread('testimage.jpg')
print('hello')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
stop = stop_cascade.detectMultiScale(gray, 5, 5)
for (x,y,w,h) in stop:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
cv2.imwrite('outputimage.jpg', img)
k = cv2.waitKey(30) & 0xff

