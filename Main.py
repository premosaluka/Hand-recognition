import numpy
import cv2
import os

video_capture = cv2.VideoCapture(0)

cam_width = 800
cam_length = 600

video_capture.set(3,cam_width)
video_capture.set(4,cam_length)

folderPath = "FingerImages"
myList = os.listdir()

while True:
	sc, img = video_capture.read()
	if sc:
		cv2.imshow("Image", img)
		cv2.waitKey(1)