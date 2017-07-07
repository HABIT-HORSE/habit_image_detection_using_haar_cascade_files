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

# import the necessary packages
import cv2
import sys
import glob
import os
import time
import datetime
import argparse
from decimal import Decimal
 

cascadesDir = 'cascades'
dataDir = 'data'
inPathPos = './posin'
outPathPos = './posout'
inPathNeg = './negin'
outPathNeg = './negout'





###############################  START parseCommandLineArguments #########################################


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("--doFlipFrame", dest='verticalFlipEachFrameForAsymetricalDetector', action='store_true', help="In addition to initial frame orientation, vertical flip frame around the Y axis and also test this against the current detector?")
ap.add_argument("--dontFlipFrame", dest='verticalFlipEachFrameForAsymetricalDetector', action='store_false', help="In addition to initial frame orientation, vertical flip frame around the Y axis and also test this against the current detector?")
ap.set_defaults(verticalFlipEachFrameForAsymetricalDetector=False)


ap.add_argument("-t", "--target",
	default="target object",
	help="name of target object")

ap.add_argument("-d", "--display",
	default="false",
	help="if detected, display query image with boundary box")

ap.add_argument("-dh", "--displayHits",
	default="false",
	help="if detected, display images that trigger detector with ROI marked up")
	
ap.add_argument("-s", "--save",
	default="true",
	help="if detected, save query image with boundary box")

args = vars(ap.parse_args())



# the tuple of file types...matching OpenCV compatible image formats
types = ('*.bmp', '*.pbm', '*.pgm', '*.ppm', '*.sr', '*.ras', '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.tiff', '*.tif', '*.png') 

###############################  END parseCommandLineArguments #########################################

logTimeStamp = datetime.datetime.now()
logTimeStamp = logTimeStamp.strftime("%Y%m%d-%H%M%S")

message = logTimeStamp + "\n\n"

print logTimeStamp + "\n\n"


###############################  START using Haar Cascade detectors #########################################

def detect(frame, frame_flipped, frame_orientation, logTimeStamp, cascade):

   
  targetDetected = False
  if frame_orientation == "flipped":   	
    gray = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2GRAY)
  else:
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
  count = 0;
	
#for cascade in glob.glob(cascadesDir + "\\*.xml"):

  #print ( glob.glob(cascadesDir + "\\*.xml") ) # list all found cascades
  #print(cascade)
  cascadename = cascade[cascade.rfind("\\") + 1:]
  cascadenameWithoutPath = os.path.splitext(cascadename)[0]
  
  #print("Trying :" + cascadenameWithoutPath + " " + str(count))
  #count += 1
	
  # load the Haar cascade detector, then detect target object in the input image
  detector = cv2.CascadeClassifier(cascade)

  targetObjects = detector.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE
  )

   # Draw a rectangle around the target objects... if any detected
  for (x, y, w, h) in targetObjects:
  
	if frame_orientation == "flipped":
		cv2.rectangle(frame_flipped, (x, y), (x+w, y+h), (0, 255, 0), 2)
	else:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	#cv2.imshow(args["target"], gray)
	#cv2.waitKey(0)
	
  if len(targetObjects) != 0:
	# print(logTimeStamp + ' - ' + cascadenameWithoutPath + ': target detected (' + frame_orientation + ')!')
	targetDetected = True
	if args["displayHits"] == "true":
		if frame_orientation == "flipped":
			cv2.imshow(args["target"] + "FLIPPED!", frame_flipped)
		else:
			cv2.imshow(args["target"], frame)
		
		cv2.waitKey(0)
		
		
		
    #if len(targetObjects) != 0:
  if targetDetected == True:
   return True
  else:
    #print('nothing in frame')
   return False

###############################  End using Haar Cascade detectors #########################################



###############################  Start using example detector #############################################

def exampleDetector(frame):

      '''
      if <detection is positive>:
       return True
      else:
       return False
      '''

###############################  End using example detector #############################################


def detectImages():

	global message 

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
			filename = imagePath[imagePath.rfind("\\") + 1:]
			frame = cv2.imread(imagePath)
			###############################  Start detecting... #############################################	
			# only proceed if target object detected
			frameDectionStatus = False
			frame_flippedDectionStatus = False
#			if args["verticalFlipEachFrameForAsymetricalDetector"] == True:
			frame_flipped = cv2.flip(frame,1) # flip frame
			
			frameDectionStatus = detect(frame, frame_flipped, "unflipped", logTimeStamp, cascade) # run detector on un-flipped frame
			
			if args["verticalFlipEachFrameForAsymetricalDetector"] == True and frameDectionStatus == False : # only check flipped if not detected in unflipped
			  print "FLIPPING...."
			  frame_flippedDectionStatus = detect(frame, frame_flipped, "flipped", logTimeStamp, cascade) # run detector on flipped frame
			
			'''
			Note: although, the detect() function takes the variable 'frame' (which is a local, not global variable), the changes made to it around line 108 (cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) ) will be reflected in the outer version of 'frame' in this While loop. So, the detected object green boxes are on this version of the frame. 
			I think that this is because the OpenCV rectangle function appends to the variable, rather than reassigning it. Probably works like this:
			If B is assigned to "cat" in the outer code (B="cat"), and then it (B) is reassigned (B = "dog") in the inner function, then the outer variable (B) remains unchanged ("cat"). 
			When the inner variable is appended to (B.append (" has run away"), then the outer variable also changes to "cat has run away".
			'''
			
			#if frameDectionStatus == False or frame_flippedDectionStatus == False:
			if frameDectionStatus == True or frame_flippedDectionStatus == True:
			# if exampleDetector(frame, "unflipped", logTimeStamp): # how to add a different detector, instead of Haar Cascades
			###############################  End detecting... ###############################################	
			      
				  if frame_flippedDectionStatus == True and frameDectionStatus == False: # if there both TRUE, then flipping the frame made no difference. Only want to label if only detected on flipped.
					frameOrientation = "flipped";
				  else: # must be either flipped == True and notFlipper == False or both are true. Either way, flipping made no difference!
					frameOrientation = "unflipped";

				  positiveDetections = positiveDetections + 1
				  print (filename + " : true(" + frameOrientation + ")\n")
				  message+= filename + " : true(" + frameOrientation + ")\n"
				  # if we are flipping frames for detection (in addition to regular detection) AND a target object has been detected in the flipped frame...			
				  if args["verticalFlipEachFrameForAsymetricalDetector"] == True and frame_flippedDectionStatus == True:
					frame = cv2.flip(frame_flipped,1) # flip frame (with marked up detected targets) back to correct orientation
				  if args["save"] == "true":
					cv2.imwrite(outPathPos + "\\" + cascadenameWithoutPath + "_" + filename, frame) # only save a new version of image with ROI / detection bounding box, if DETECTED
					print ("Saving copy of " + filename + " with detection marked...")
					message+= "Saving copy of " + filename + " with detection marked...\n"
			else:
				#negativeDetections = negativeDetections + 1
				print (filename + " : false")
				message+= filename + " : false\n"
		
			if args["display"] == "true":
			# show the detected target object
				cv2.imshow(args["target"], frame)
				cv2.waitKey(0)

####################### START TESTING NEGATIVE IMAGES ##################################################################				
				
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
			frame = cv2.imread(imagePath)
			

				###############################  Start detecting... #############################################	
			# only proceed if target object detected
			
			frameDectionStatus = False
			frame_flippedDectionStatus = False
			
			#if args["verticalFlipEachFrameForAsymetricalDetector"] == True:
			frame_flipped = cv2.flip(frame,1) # flip frame
			
			frameDectionStatus = detect(frame, frame_flipped, "unflipped", logTimeStamp, cascade) # run detector on un-flipped frame
			
			if args["verticalFlipEachFrameForAsymetricalDetector"] == True and frameDectionStatus == False : # only check flipped if not detected in unflipped
			  print "FLIPPING...."
			  frame_flippedDectionStatus = detect(frame, frame_flipped, "flipped", logTimeStamp, cascade) # run detector on flipped frame
			
			'''
			Note: although, the detect() function takes the variable 'frame' (which is a local, not global variable), the changes made to it around line 108 (cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) ) will be reflected in the outer version of 'frame' in this While loop. So, the detected object green boxes are on this version of the frame. 
			I think that this is because the OpenCV rectangle function appends to the variable, rather than reassigning it. Probably works like this:
			If B is assigned to "cat" in the outer code (B="cat"), and then it (B) is reassigned (B = "dog") in the inner function, then the outer variable (B) remains unchanged ("cat"). 
			When the inner variable is appended to (B.append (" has run away"), then the outer variable also changes to "cat has run away".
			'''
			
			#if frameDectionStatus == False or frame_flippedDectionStatus == False:
			if frameDectionStatus == True or frame_flippedDectionStatus == True:
			# if exampleDetector(frame, "unflipped", logTimeStamp): # how to add a different detector, instead of Haar Cascades
		###############################  End detecting... ###############################################	

			  if frame_flippedDectionStatus == True and frameDectionStatus == False: # if there both TRUE, then flipping the frame made no difference. Only want to label if only detected on flipped.
			    frameOrientation = "flipped";
			  else: # must be either flipped == True and notFlipper == False or both are true. Either way, flipping made no difference!
			    frameOrientation = "unflipped";

		
			  falseAlarms = falseAlarms + 1
			  print (filename + " : true(" + frameOrientation + ")\n")
			  message+= filename + " : true(" + frameOrientation + ")\n"
			  # if we are flipping frames for detection (in addition to regular detection) AND a target object has been detected in the flipped frame...			
			  if args["verticalFlipEachFrameForAsymetricalDetector"] == True and frame_flippedDectionStatus == True:
				frame = cv2.flip(frame_flipped,1) # flip frame (with marked up detected targets) back to correct orientation
			  if args["save"] == "true":
			   cv2.imwrite(outPathNeg + "\\" + cascadenameWithoutPath + "_" + filename, frame) # only save a new version of image with ROI / detection bounding box, if DETECTED
			   print ("Saving copy of " + filename + " with detection marked...")
			   message+= "Saving copy of " + filename + " with detection marked...\n"
			else:
			#negativeDetections = negativeDetections + 1
			  print (filename + " : false")
			  message+= filename + " : false\n"
		
			if args["display"] == "true":
			# show the detected target object
			 cv2.imshow(args["target"], frame)
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


detectImages()
	
	