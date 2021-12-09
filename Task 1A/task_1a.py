'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 1A of Berryminator(BM) Theme (eYRC 2021-22).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1263 ]
# Author List:		[ Names of team members worked on this file separated by Comma: Trevor Dcosta, Malcolm Dias, Adithya Basker,Sumedh Chinchmalatpure ]
# Filename:			task_1a.py
# Functions:		detect_shapes
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def color_difference (color1, color2):
	return sum([abs(component1-component2) for component1, component2 in zip(color1, color2)])
##############################################################

def detect_shapes(img, ):
	"""
		Purpose:
		---
		This function takes the image as an argument and returns a nested list
		containing details of colored (non-white) shapes in that image
		Input Arguments:
		---
		`img` :	[ numpy array ]
				numpy array of image returned by cv2 library
		Returns:
		---
		`detected_shapes` : [ list ]
				nested list containing details of colored (non-white)
				shapes present in image

		Example call:
		---
		shapes = detect_shapes(img)
		"""
	detected_shapes = []

	##############	ADD YOUR CODE HERE	##############
	imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, binary = cv2.threshold(imgGry, 220, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours=contours[1:]

	for contour in contours:
		shape = None
		color = None
		cX,cY = 0,0
		epsilon = 0.03 * cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour,epsilon , True)
		if len(approx) == 3:
			shape = "Triangle"
		elif len(approx) == 4:
			rect = cv2.minAreaRect(approx)
			w,h = rect[1]
			aspectRatio = float(w / h)
			if aspectRatio < 0.95 or aspectRatio > 1.05:
				shape = "Rectangle"
			else:
				shape = "Square"
		elif len(approx) == 5:
			shape = "Pentagon"
		else:
			shape = "Circle"

		M = cv2.moments(contour)
		cX = int(M['m10'] / M['m00'])
		cY = int(M['m01'] / M['m00'])

		b,g,r = img[cY,cX]
		if (b>250) and (g<5) and (r<5):
			color ="Blue"
		elif (b<5) and (g>250) and (r<5):
			color = "Green"
		elif (b<5) and (g<5) and (r>250):
			color = "Red"
		elif (b<5) and (g>135)and(g<155) and (r>250):
			color = "Orange"
		else:
			pass

		detected_shapes.append([color, shape, (cX, cY)])

	##################################################

	return detected_shapes

def get_labeled_image(img, detected_shapes):
	######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########
	"""
	Purpose:
	---
	This function takes the image and the detected shapes list as an argument
	and returns a labelled image
	Input Arguments:
	---
	`img` :	[ numpy array ]
			numpy array of image returned by cv2 library
	`detected_shapes` : [ list ]
			nested list containing details of colored (non-white)
			shapes present in image
	Returns:
	---
	`img` :	[ numpy array ]
			labelled image

	Example call:
	---
	img = get_labeled_image(img, detected_shapes)
	"""
	######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

	for detected in detected_shapes:
		colour = detected[0]
		shape = detected[1]
		coordinates = detected[2]
		cv2.putText(img, str((colour, shape)), coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
	return img

if __name__ == '__main__':

	# path directory of images in 'test_images' folder
	img_dir_path = 'test_images/'

	# path to 'test_image_1.png' image file
	file_num = 1
	img_file_path = img_dir_path + 'test_image_' + str(file_num) + '.png'

	# read image using opencv
	img = cv2.imread(img_file_path)

	print('\n============================================')
	print('\nFor test_image_' + str(file_num) + '.png')

	# detect shape properties from image
	detected_shapes = detect_shapes(img)
	print(detected_shapes)

	# display image with labeled shapes
	img = get_labeled_image(img, detected_shapes)
	cv2.imshow("labeled_image", img)
	cv2.waitKey(2000)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 16):

			# path to test image file
			img_file_path = img_dir_path + 'test_image_' + str(file_num) + '.png'

			# read image using opencv
			img = cv2.imread(img_file_path)

			print('\n============================================')
			print('\nFor test_image_' + str(file_num) + '.png')

			# detect shape properties from image
			detected_shapes = detect_shapes(img)
			print(detected_shapes)

			# display image with labeled shapes
			img = get_labeled_image(img, detected_shapes)
			cv2.imshow("labeled_image", img)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()