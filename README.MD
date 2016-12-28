
Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham

A benchmarking and test utility for haar cascades (OpenCV XML format) object detectors.

Run the cascade on the included positive and negative image sets and get the resulting hit rate and false alarm count.

The following image types (those supported by OpenCV) are supported: bmp, pbm pgm, ppm, sr, ras, jpeg, jpg, jpe, jp2, tiff, tif, png.

Put one or more XML cascade files into the cascades directory and run. Any XML files will be picked up from this directory.

Example Python command: detect.py --target my_target_object --display false --save false

The target is a text string (no whitespace) which is the name of an object that you would like to detect.
default="target object"

If the display argument is set to 'true', then each image will display, along with its bounding box / ROI. Press [Enter] to move to the next image.
default="false"

If the save argument is set to 'true', then each positively detected image will be saved, along with its bounding box / ROI.
default="true",

A data text file will be saved in the data directory, with the results of the test.

