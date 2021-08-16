import math
from scipy import ndimage
import cv2
import numpy as np

def getRegionOfInterest(frame):

	print(frame.size)
	kernel = np.ones((14,14), np.uint8)

	#Apply bilateral filter to the frame
	frame = cv2.bilateralFilter(frame, 9, 75, 75)

	#Convert from BGR colour space to grayscale
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#Apply canny edge detection and dilation+erosion to connect gaps in edges
	canny = cv2.Canny(gray_frame, 75, 150, 1)
	canny = cv2.dilate(canny, kernel, 1)
	canny = cv2.erode(canny, kernel, 1)

	# #Find hough lines to orientate the image
	# lines = cv2.HoughLines(canny, 1, np.pi / 180, 200, None, 0, 0)
	# cdst = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

	# angles = []
	# if lines is not None:
	# 	for i in range(0, len(lines)):
	# 		rho = lines[i][0][0]
	# 		theta = lines[i][0][1]
	# 		a = math.cos(theta)
	# 		angles.append(180*theta/3.1415926)
	# 		print(180*theta/3.1415926)
	# 		b = math.sin(theta)
	# 		x0 = a * rho
	# 		y0 = b * rho
	# 		pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
	# 		pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
	# 		cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
	
	# cv2.imshow('Hough lines', cdst)

	
	# angles_np = np.array(angles)

	# if angles_np.mean() < 90:
	# 	filter_arr = angles_np < 90
	# else:
	# 	filter_arr = angles_np > 90

	# filtered_angles = angles_np[filter_arr]
	# canny = ndimage.rotate(canny, filtered_angles.mean())
	# cv2.imshow('Hough lines - rectified', canny)

	#Find contours
	contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if len(contours) == 2 else contours[1]

	#Find the largest bounding rectangle
	largest_rec = 0
	x = y = w = h = 0
	x_max = y_max = w_max = h_max = 0
	for c in contours:
		x,y,w,h = cv2.boundingRect(c)
		if w*h > largest_rec:
			largest_rec = w*h
			x_max, y_max, w_max, h_max = x,y,w,h

	return (x_max, y_max, w_max, h_max, frame)