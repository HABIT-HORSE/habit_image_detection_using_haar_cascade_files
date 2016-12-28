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
default="false",
	
"-s", "--save" = if detected, save query image with boundary box
default="true",

:comment

detect.py --target horse_ears --display false --save true
pause