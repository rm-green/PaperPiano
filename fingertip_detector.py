import cv2
import hand_detector

def fingertip_detector(frame, background_subtractor):

	frame = frame.copy()
	bottom_extreme = None

	#The hand mask created by KNN background subtraction
	hand_mask = hand_detector.hand_detector(frame, background_subtractor)

	#Gets the contours of the image
	contours, _ = cv2.findContours(hand_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if(len(contours) > 0):
		#Get the biggest contour
		biggest_contour = max(contours, key = cv2.contourArea)

		#Define a minimum size for the contour to prevent false positives
		if(cv2.contourArea(biggest_contour) < 500):
			return frame, bottom_extreme

		#Finds the bottom point (extreme) of the contour
		bottom_extreme = tuple(biggest_contour[biggest_contour[:, :, 1].argmax()][0])

		#Creates the convex hull from the contour
		hull_list = []
		hull = cv2.convexHull(biggest_contour)
		hull_list.append(hull)

		#Drawn the convex hull on the frame and a circle at the bottom extreme
		color = (0, 255, 0)
		cv2.drawContours(frame, hull_list, 0, color)
		cv2.circle(frame, bottom_extreme, 8, (0, 255, 0), -1)

	
	return frame, bottom_extreme
	