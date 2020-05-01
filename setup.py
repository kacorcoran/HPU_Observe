"""
-------------------------------------------------------------------------------------------
setup.py --- file sturcture setup for HPU_Reduce
Kyle Corcoran - University of Virginia
kac8aj@virginia.edu
2020
-------------------------------------------------------------------------------------------
This code creates the directories necessary for HPU_Reduce, and it will also remove
the files that are not necessary to run HPU_Reduce.  This includes the README.md file,
so you will want to view this on the github page as it will be easier to see anyway.
If you would like to modify the file structure, you can do so here or in HPU_Reduce.py.

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
        -logs
        -data_sheets
     ⃝ plots
Removes the following files if they exist:
     ⃝ logo.png
     ⃝ file_tree.png
     ⃝ README.md
     ⃝ LICENSE
"""

import os

# ------------------------  Lists of files to be removed  ------------------------ #
rm_files = ["logo.png","file_tree.png","README.md","LICENSE"]

# ------------------------  Lists of directories to be created  ------------------------ #
# intermediate directories
int_dirs = ["raw_frames","cal_frames","red_frames","file_outputs","plots"]
# calibration subdirectories
cal_dirs = ["bias_frames","dark_frames","flat_frames"]
out_dirs = ["logs","data_sheets"]
# ---- add additional lists if you want other subdirectories

# ------------------------  Remove specified files  ------------------------ #
for file in rm_files:
    if(os.path.exists(file)==True):
        os.remove(file)

# ------------------------  Create intermediate directories  ------------------------ #
for int_dir in int_dirs:
    os.makedirs(int_dir, exist_ok=True)

# ------------------------  Create subdirectories  ------------------------ #
# calibrations
for cal_dir in cal_dirs:
    os.makedirs(f'cal_frames/{cal_dir}', exist_ok=True)
for out_dir in out_dirs:
    os.makedirs(f'file_outputs/{out_dir}', exist_ok=True)
# ---- copy, paste, and change the intermediate directory and list name to make any additonal subdirectories
