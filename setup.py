"""
-------------------------------------------------------------------------------------------
setup.py --- file sturcture setup for HPU_Reduce
Kyle Corcoran - University of Virginia
kac8aj@virginia.edu
2020
-------------------------------------------------------------------------------------------
This code creates the directories necessary for HPU_Reduce.
If you would like to modify the file structure, you can do so here or in HPU_Reduce.py

This does assume you have cloned the github repository into the directory that you wish to
run everything in.  If you accidentally clone it somewhere else, you can move the files
and directories or add a path in the HPU_Reduce.py code.
-------------------------------------------------------------------------------------------
Creates the following directories for use by HPU_Reduce:
     ⃝ raw_frames
     ⃝ cal_frames
        - bias_frames
        - dark_frames
        - flat_frames
     ⃝ red_frames
     ⃝ file_outputs
     ⃝ plots
"""

import os
# ------------------------  Lists of directories to be created  ------------------------ #
# intermediate directories
int_dirs = ["raw_frames","cal_frames","red_frames","file_outputs","plots"]
# calibration subdirectories
cal_dirs = ["bias_frames","dark_frames","flat_frames"]
# ---- add additional lists if you want other subdirectories

# ------------------------  Create intermediate directories  ------------------------ #
for int_dir in int_dirs:
    os.makedirs(int_dir, exist_ok=True)

# ------------------------  Create subdirectories  ------------------------ #
# calibrations
for cal_dir in cal_dirs:
    os.makedirs(f'cal_frames/{cal_dir}', exist_ok=True)
# ---- copy, paste, and change the intermediate directory and list name to make any additonal subdirectories
