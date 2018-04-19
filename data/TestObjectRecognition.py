# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)

stop_cascade = cv2.CascadeClassifier('cascade.xml')

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image - this array
	# will be 3D, representing the width, height, and # of channels
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stop = stop_cascade.detectMultiScale(gray, 10, 10)
        print(stop)
        for (x,y,w,h) in stop:
              print('Stop Sign Detected')
              font = cv2.FONT_HERSHEY_SIMPLEX
              image = cv2.putText(image,'Stop Sign',(x-w,y-h), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
	# show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
             break
cv2.destroyAllWindows()
