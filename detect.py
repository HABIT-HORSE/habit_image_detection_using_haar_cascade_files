'''
Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham

'''

inPathPos = './posin'
outPathPos = './posout'

inPathNeg = './negin'
outPathNeg = './negout'

cascadesDir = 'cascades'

dataDir = 'data'

# import the necessary packages
import argparse
import cv2
import glob
from decimal import Decimal
import os
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

'''
ap.add_argument("-c", "--cascade",
	default= cascadesDir + "\\cascade.xml",
	help="path to detector haar cascade XML file")
'''
	
ap.add_argument("-t", "--target",
	default="target object",
	help="name of target object")

ap.add_argument("-d", "--display",
	default="false",
	help="if detected, display query image with boundary box")
	
ap.add_argument("-s", "--save",
	default="true",
	help="if detected, save query image with boundary box")

args = vars(ap.parse_args())

message = ""

# the tuple of file types...matching OpenCV compatible image formats
types = ('*.bmp', '*.pbm', '*.pgm', '*.ppm', '*.sr', '*.ras', '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.tiff', '*.tif', '*.png') 


for cascade in glob.glob(cascadesDir + "\\*.xml"):

	pos_files_grabbed = []

	positiveDetections = 0

	cascadename = cascade[cascade.rfind("\\") + 1:]
	
	cascadenameWithoutPath = os.path.splitext(cascadename)[0]
	
	print "\n"
	message+= "\n"
	print "#############################" + cascadename + "#############################"
	message+= "#############################" + cascadename + "#############################\n"
	print "\n"
	message+= "\n"
	
	print "Positive images\n"
	message+= "\n"
		
	for files in types:
		pos_files_grabbed.extend(glob.glob(inPathPos + "\\" + files))
	for imagePath in pos_files_grabbed:
	#for imagePath in glob.glob(inPathPos + "\*.jpg"): # for loading all images of specific format
		thisImageContainsDetection = False
		filename = imagePath[imagePath.rfind("\\") + 1:]
		image = cv2.imread(imagePath)
		# load the input image and convert it to grayscale
		# image = cv2.imread(args["image"])
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# load the Haar cascade detector, then detect target object in the input image
		detector = cv2.CascadeClassifier(cascade)
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
		# loop over the detected target objects and draw a rectangle surrounding each
		for (i, (x, y, w, h)) in enumerate(rects):
			thisImageContainsDetection = True
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			#cv2.putText(image, args["target"] + "#{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
		if thisImageContainsDetection == True:
			positiveDetections = positiveDetections + 1
			print (filename + " : true")
			message+= filename + " : true\n"
			if args["save"] == "true":
				cv2.imwrite(outPathPos + "\\" + cascadenameWithoutPath + "_" + filename, image) # only save a new version of image with ROI / detection bounding box, if DETECTED
				print ("Saving copy of " + filename + " with detection marked...")
				message+= "Saving copy of " + filename + " with detection marked...\n"
		else:
			#negativeDetections = negativeDetections + 1
			print (filename + " : false")
			message+= filename + " : false\n"
		
		if args["display"] == "true":
			# show the detected target object
			cv2.imshow(args["target"], image)
			cv2.waitKey(0)


	neg_files_grabbed = []

	falseAlarms = 0

	print "\n"
	message+= "\n"
	print "Negative images\n"
	message+= "\n"
	
	for files in types:
		neg_files_grabbed.extend(glob.glob(inPathNeg + "\\" + files))
	for imagePath in neg_files_grabbed:
	#for imagePath in glob.glob(inPathPos + "\*.jpg"): # for loading all images of specific format
		thisImageContainsDetection = False
		filename = imagePath[imagePath.rfind("\\") + 1:]
		image = cv2.imread(imagePath)
		# load the input image and convert it to grayscale
		# image = cv2.imread(args["image"])
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# load the Haar cascade detector, then detect target object in the input image
		detector = cv2.CascadeClassifier(cascade)
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
		# loop over the detected target objects and draw a rectangle surrounding each
		for (i, (x, y, w, h)) in enumerate(rects):
			thisImageContainsDetection = True
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			cv2.putText(image, args["target"] + "#{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
		if thisImageContainsDetection == True:
			#positiveDetections = positiveDetections + 1
			falseAlarms = falseAlarms + 1
			print (filename + " : true")
			message+= filename + " : true\n"
			if args["save"] == "true":
				cv2.imwrite(outPathNeg + "\\" + cascadenameWithoutPath + "_" + filename, image) # only save a new version of image with ROI / detection bounding box, if DETECTED
				print ("Saving copy of " + filename + " with detection marked...")
				message+= "Saving copy of " + filename + " with detection marked...\n"
		else:
			#falseAlarms = falseAlarms + 1
			print (filename + " : false")
			message+= filename + " : false\n"
		
		if args["display"] == "true":
			# show the detected target object
			cv2.imshow(args["target"], image)
			cv2.waitKey(0)
		
			
	positivePercentage = round(  ( Decimal( positiveDetections ) / len(pos_files_grabbed) ) * 100, 2) 
	negativePercentage = round(  ( Decimal( falseAlarms ) / len(neg_files_grabbed) ) * 100, 2) 

	print "\n"
	message+= "\n"
	print ("Hit Rate: " + str(positiveDetections) + " out of " + str(len(pos_files_grabbed)) + ": " + str(positivePercentage) + "%" )
	message+= "Hit Rate: " + str(positiveDetections) + " out of " + str(len(pos_files_grabbed)) + ": " + str(positivePercentage) + "%\n"
	print ("False Alarms: " + str(falseAlarms) + " out of " + str(len(neg_files_grabbed)) + ": " + str(negativePercentage) + "%")
	message+= "False Alarms: " + str(falseAlarms) + " out of " + str(len(neg_files_grabbed)) + ": " + str(negativePercentage) + "%\n"

#print (message)

text_file = open(dataDir + "\\" + "data.txt", "w")
text_file.write(message)
text_file.close()
