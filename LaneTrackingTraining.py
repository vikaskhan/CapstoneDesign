import curses
import pyfirmata
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
from tempfile import TemporaryFile

frame_count = 195


def storeData(image, key):
        if frame_count == 0:
                np.save("training_data/output" + str(frame_count), key)
                global frame_count
                frame_count += 1
                return
        if frame_count != 0:
                np.save("training_data/input" + str(frame_count-1), image)
                np.save("training_data/output" + str(frame_count), key)
                global frame_count                
                frame_count += 1               
                return
def main():

	#camera setup
	camera = PiCamera()
	camera.resolution = (320,240)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size = (320,240))

	time.sleep(2)

	board = pyfirmata.Arduino('/dev/ttyUSB0')
	pin4 = board.get_pin('d:4:o')
	pin5 = board.get_pin('d:5:o')
	pin6 = board.get_pin('d:6:p')
	pin9 = board.get_pin('d:9:o')
	pin10 = board.get_pin('d:10:o')
	pin11 = board.get_pin('d:11:p')

	pin4.write(1)
	pin5.write(0)
	pin6.write((float(0.6))) #right
	pin9.write(1)
	pin10.write(0)
	pin11.write(float(0.6)) #left

	stdscr = curses.initscr()
	curses.cbreak()
	stdscr.keypad(1)


	right_count = 0
	left_count = 0
	up_count = 0
	down_count = 0
	up = np.array([1, 0, 0, 0])
	right = np.array([0,1,0,0])
	left = np.array([0,0,1,0])
	down = np.array([0,0,0,1])

	stdscr.refresh()
	key = ''
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		if key == ord('q'):
			np.save("training_data/input" + str(frame_count-1), image)
			break

		#get image from stream
		image = frame.array
		key = stdscr.getch()
		stdscr.addch(20,25,key)
		stdscr.refresh()
		if key == curses.KEY_UP:
			pin6.write((float(0.6))) #right
			pin11.write(float(0.6)) #left
			stdscr.addstr(2, 10, "Up")
			storeData(image, up)
			prev = up
			up_count+=1
		elif key == curses.KEY_RIGHT:
			stdscr.addstr(2, 10, "Right")
			pin6.write((float(0.15))) #right
			pin11.write(float(0.6)) #left
			storeData(image, right)
			prev = right
			right_count+=1
		elif key == curses.KEY_LEFT: 
			stdscr.addstr(2, 10, "Left")
			pin6.write((float(0.6))) #right
			pin11.write(float(0.15)) #left
			storeData(image,left)
			prev = left
			left_count+=1
		elif key == curses.KEY_DOWN: 
			stdscr.addstr(2, 10, "Down")
			pin6.write((float(0))) #right
			pin11.write(float(0)) #left
			storeData(image, down)
			prev = down
			down_count+=1
		stdscr.addstr(4, 10, str(up_count))
		stdscr.addstr(5, 10, str(right_count))
		stdscr.addstr(6, 10, str(left_count))
		stdscr.addstr(7, 10, str(down_count))
		rawCapture.truncate(0)

	curses.endwin()

if __name__ == "__main__":
        main()

