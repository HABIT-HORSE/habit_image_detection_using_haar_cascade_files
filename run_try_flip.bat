goto comment

Author:  Steve North
Author URI:  http://www.cs.nott.ac.uk/~pszsn/
License: AGPLv3 or later
License URI: http://www.gnu.org/licenses/agpl-3.0.en.html
Can: Commercial Use, Modify, Distribute, Place Warranty
Can't: Sublicence, Hold Liable
Must: Include Copyright, Include License, State Changes, Disclose Source

Copyright (c) 2016, The University of Nottingham

Command line options:

"-t", "--target" = name of target object
default="target object"

"-d", "--display" = if detected, display query image with boundary box
default="false"
	
"-s", "--save" = if detected, save query image with boundary box
default="true"

"-dh", "--displayHits" = if detected, display images that trigger detector with ROI marked up
default="false"

--doFlipFrame If the doFlipFrame argument is specified (no value required) then, in addition to initial image orientation, if there isn't a hit, then the image will be vertically flipped around the vertical axis and retested. If not specified, then images will not be flipped.
default="false"

:comment

detect.py --target horse_ears --display false --displayHits false --save true --doFlipFrame
pause