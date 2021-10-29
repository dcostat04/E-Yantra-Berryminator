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

##############################################################

def detect_shapes(img):
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
	
	##############	ADD YOUR CODE HERE	##############
	detected_shapes = []
	lower = {'red': ([166, 84, 141]), 'green': ([50, 50, 120]), 'blue': ([80, 10, 0]), 'yellow': ([23, 59, 119]),
			 'orange': ([0, 50, 80]), 'purple': ([130, 80, 80])}  # assign new item lower['blue'] = (93, 10, 0)
	upper = {'red': ([186, 255, 255]), 'green': ([70, 255, 255]), 'blue': ([128, 255, 255]), 'yellow': ([54, 255, 255]),
			 'orange': ([20, 255, 255]), 'purple': ([150, 255, 255])}


	blurred = cv2.GaussianBlur(img, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mlist = []
	clist = []
	ks = []

	for (key, value) in upper.items():

		kernel = np.ones((2, 2), np.uint8)
		mask = cv2.inRange(hsv, np.array(lower[key]), np.array(upper[key]))
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		mask = cv2.dilate(mask, kernel, iterations=1)
		mlist.append(mask)
		cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(cnts) >= 1:
			clist.append(cnts[-1])
			ks.append(key)

	for i, cnt in enumerate(clist):
		kg = []
		peri = cv2.arcLength(cnt, True)
		vertices = cv2.approxPolyDP(cnt, 0.04 * peri, True)
		approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
		cv2.drawContours(img, [approx], 0, (0, 0, 0), 5) 

		M = cv2.moments(cnt)

		if len(vertices) == 3:
			objectType = ' Triangle'
			obj=ks[i]
		elif len(vertices) == 4:
			x1, y1, w, h = cv2.boundingRect(vertices)
			aspectRatio = float(w) / h
			if aspectRatio >= 0.95 and aspectRatio <= 1.05:
				objectType = 'Square'
				obj = ks[i]
			else:
				objectType = 'Rectangle'
				obj = ks[i]
		elif len(vertices) == 5:
			objectType = 'Pentagon'
			obj = ks[i]
		else:
			objectType = 'Circle'
			obj = ks[i]

		kg.append(obj)
		kg.append(objectType)
		cX = int(M['m10'] / M['m00'])
		cY = int(M['m01'] / M['m00'])
		gg = (cX, cY)
		kg.append(gg)
		detected_shapes.append(kg)
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
		cv2.putText(img, str((colour, shape)),coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
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
