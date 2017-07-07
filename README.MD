
Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016-2017, The University of Nottingham

A benchmarking and test utility for haar cascades (OpenCV XML format) object detectors.

This tool was developed for the HABIT (Horse Automated Behaviour Identification Tool) project.

Run the cascade on the included positive and negative image sets and get the resulting hit rate and false alarm count.

The following image types (those supported by OpenCV) are supported: bmp, pbm pgm, ppm, sr, ras, jpeg, jpg, jpe, jp2, tiff, tif, png.

Put one or more XML cascade files into the cascades directory and run. Any XML files will be picked up from this directory.

Example Python command: detect.py --target horse_ears --display false --displayHits false --save true --doFlipFrame

Note: there are 3 Windows .bat files showing examples.

The target is a text string (no whitespace) which is the name of an object that you would like to detect.
default="target object"

If the display argument is set to 'true', then each image will display, along with its bounding box / ROI. Press [Enter] to move to the next image.
default="false"

If the displayHits argument is set to 'true', then each positively detected image will be displayed with ROI marked up
default="false"

If the save argument is set to 'true', then each positively detected image will be saved, along with its bounding box / ROI.
default="true"

If the doFlipFrame argument is specified (no value required) then, in addition to initial image orientation, if there isn't a hit, then the image will be vertically flipped around the vertical axis and retested. If not specified, then images will not be flipped.

A data text file will be saved in the data directory, with the results of the test.

The positive and negative images are made up of all of the items in: the HABIT horses still image detector testing dataset 200 [1]. Other image datasets were also added. 

This was substantially recoded in July 2017, to add the feature to flip each image vertically (around the vertical axis) and retest, if an object isn't detected without flipping. 


Two detectors come with this program (in the directory \cascades\ ): horse_uddin_and_ayaz_2016_right_facing_side_view.xml [2] and habit_haar_cascade_horse_ears_1.xml [3].

[1] Steve North, 2017. HABIT horses still image detector testing dataset 200.  http://dx.doi.org/10.5281/zenodo.822853.

[2] MS Uddin and AY Akhi, 2016. Horse Detection Using Haar Like Features. International Journal of Computer Theory and Engineering 8, 5, 415.

[3] Steve North. 2017. Software Program: HABIT haar cascade horse ears 1.doi:10.5281/zenodo.823354. Available from: https://doi.org/10.5281/zenodo.823354.



