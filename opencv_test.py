import sys
import cv2
import video_cropper
import fingertip_detector
import fingertip_tracker
from imutils.video import WebcamVideoStream
from collections import deque
import pygame.mixer

pygame.mixer.init()
noteC = pygame.mixer.Sound('./Notes/C.ogg')
noteD = pygame.mixer.Sound('./Notes/D.ogg')
noteE = pygame.mixer.Sound('./Notes/E.ogg')
noteF = pygame.mixer.Sound('./Notes/F.ogg')
noteG = pygame.mixer.Sound('./Notes/G.ogg')
noteA = pygame.mixer.Sound('./Notes/A.ogg')
noteB = pygame.mixer.Sound('./Notes/B.ogg')
cap = WebcamVideoStream(src=2).start()

if cap is None:
	print('Error opening video stream!')
	sys.exit(1)
frame = cap.read()
x, y, w, h, firstFrame = video_cropper.getRegionOfInterest(frame)
background_subtractor = cv2.createBackgroundSubtractorKNN(history=1500)
tracker = fingertip_tracker.fingertip_tracker()

def TouchDetector():
	while True:
		frame = cap.read()

		# skin = cv2.bitwise_and(frame, frame, mask = fgMask)
		# show the skin in the image along with the mask
		# cv2.imshow("images", np.hstack([frame, skin]))
		cropped = frame[y:y+h, x:x+w]
		#cv2.imshow('cropped', cropped)
		hulls, fingertip_position = fingertip_detector.fingertip_detector(cropped, background_subtractor)
		
		cv2.imshow('hull', hulls)

		is_clicking = tracker.track_fingertip(fingertip_position)
		sound = noteA
		if(is_clicking):
			sound.play()
		else:
			sound.stop()
		
		print(cap.stream.get(cv2.CAP_PROP_FPS))
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	cap.stream.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	TouchDetector()
