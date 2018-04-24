import numpy as np
import pyfirmata
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import RPi.GPIO as GPIO
from threading import Thread
import socket

#setup socket
host = '159.89.53.176'
port = 500
mySocket = socket.socket()
mySocket.connect((host,port))

#Camera Setup
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 240))

#Ultrasonic Sensor Setup
GPIO.setmode(GPIO.BCM)
TRIG = 23 
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
GPIO.output(TRIG, True)
GPIO.output(TRIG, False)

#Arduino Controls Setup
board = pyfirmata.Arduino('/dev/ttyUSB0')
pin4 = board.get_pin('d:4:o')
pin5 = board.get_pin('d:5:o')
pin6 = board.get_pin('d:6:p')
pin9 = board.get_pin('d:9:o')
pin10 = board.get_pin('d:10:o')
pin11 = board.get_pin('d:11:p')

#Cascade Import 
stop_cascade = cv2.CascadeClassifier('data/cascade.xml')

# allow the camera to warmup
time.sleep(0.1)

#Global Variables
stop = False
collision = False 
control = 3
loop = 0

def lane_tracking(img):
	global mySocket
	np.save('message', img)
	file = open('message', 'rb')
	message = file.read(1024)
	while message:
		mySocket.send(message)
		message = file.read(1024)
	data = mySocket.recv(10).decode()
	print(data)


def object_recognition(img):
	stop_sign = stop_cascade.detectMultiScale(gray, 10, 10)
	for (x,y,w,h) in stop_sign:
		global stop 
		stop = True
		print('Stop Sign Detected')
		
def collision_avoidance():
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()
		
	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150
	distance = round(distance, 2)
	if distance < 15:
		global collision 
		collision = True
		print("Object Detected")
	else: 
		global collision 
		collision = False
		
def stop():
	global pin6
	global pin11
	pin6.write((float(0))) #right
	pin11.write(float(0)) #left
	
def left():
	global pin6
	global pin11
	pin6.write((float(0.6))) #right
	pin11.write(float(0.15)) #left
	
def right():
	global pin6
	global pin11
	pin6.write((float(0.15))) #right
	pin11.write(float(0.6)) #left
	
def straight():
	global pin6
	global pin11
	pin6.write((float(0.6))) #right
	pin11.write(float(0.6)) #left

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	print('Iteration: ' + str(loop))

	image = frame.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	#Create Threads
	thread1 = Thread(target = lane_tracking, args = (image,))
	thread2 = Thread(target = object_recognition, args = (gray,))
	thread3 = Thread(target = collision_avoidance)
	
	#Start Threads
	thread1.start()
	thread2.start()
	thread3.start()
	
	#Wait for Threads to exit
	thread1.join()
	thread2.join()
	thread3.join()
	
	while collision == True:
		stop()
		collision_avoidance()
	if stop == True:
		stop()
		time.sleep(3)
		straight()
	if control == 0:
		straight()
		print('straight')
	elif control == 1:
		right()
		print('right')
	elif control == 2:
		left()
		print('left')
	else:
		stop()
		print('stop')
	#Clear video stream
	rawCapture.truncate(0)
	


	
	
