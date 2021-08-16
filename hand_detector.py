import cv2
import numpy as np

def hand_detector(cropped, background_subtractor):


	#Gaussian Blur to denoise image
	cropped = cv2.GaussianBlur(cropped, (5,5), 1)

	#Apply background subtraction to create a mask of the hand
	hand_mask = background_subtractor.apply(cropped)

	#Apply erosion and dilation to create a smoother mask
	hand_mask = cv2.erode(hand_mask, (6,6))
	hand_mask = cv2.dilate(hand_mask, (7,7))

	return hand_mask

	#MIXTURE OF GAUSSIANS
	#Too noisy, recognises hand as part of the background if it is still for too long (long press)

	# backSub = cv2.createBackgroundSubtractorMOG2()
	# fgMask = backSub.apply(cropped)

	#ABSOLUTE DIFFERENCE
	#Lines from the background cause interference with the foreground mask

	# subtracted = 255 - cv2.absdiff(firstFrame, cropped)
	# grayFrame = cv2.cvtColor(subtracted, cv2.COLOR_BGR2GRAY)
	# blurred = cv2.blur(grayFrame, (8,8))

	# ret, thresholded = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY_INV)

	# eroded = cv2.erode(thresholded, (1,1))
	# dilated = cv2.dilate(eroded, (1,1))

	# cnts, heir = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# if len(cnts) > 0:
	# 	c = max(cnts, key = cv2.contourArea)
	# 	if cv2.contourArea(c) > 100:
	# 		grayFrame = cv2.drawContours(grayFrame, [c], -1, (0,255,0), 3)