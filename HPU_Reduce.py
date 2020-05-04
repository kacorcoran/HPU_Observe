"""
HPU_Reduce --- The Helpful Photometric Uranoscopy Reduction and Analysis Code
Kyle Corcoran - University of Virginia
kac8aj@virginia.edu
2020
----------------------------------------------------------------------------------------------------------
Prerequisites:
    1) Written for Python 3 with packages that depend on at least Python 3.5
    2) Installation of the following packages (assuming they are not already installed or default):
        ⃝ tqdm
        ⃝ astropy (this is probably gonna cause a numpy error with photutils at some point)
        ⃝ ccdproc
        ⃝ photutils
----------------------------------------------------------------------------------------------------------
File Structure Setup:
    Run the setup.py file in the repository to create the directories necessary for HPU_Reduce.
    I have included the same directory creation code here as some "dummy proofing", but it will print
    a message giving you a light scolding for making it run the code here.

    Remove/correct any frames that are not usable/incorrect and then place all USEABLE frames into the
    same directory as HPU_Reduce.  The code will then read in and sort all of the files into their
    respective directories before executing the rest of the code.
    ...................................................................................
    Key:
    (T) = Top directory   (I) = Middle/Intermediate directory   (S) = Bottom directory
    ...................................................................................
    (T) Directory in your desired location where you place HPU_Reduce.py
        (I) raw_frames
             ⃝ raw science frames will be placed here
                - This assumes you have removed images which are not usable
                  (e.g., smearing from telescope bump)
        (I) cal_frames
             ⃝ calibration frames will be placed here and sorted into their subdirectories
                - Leave this directory empty if you have not taken cals yet
                - This assumes you have removed images which are not usable or have incorrect headers
                  (e.g., didn't change the file type to 'bias' so the bias frame has a 'flat' file type)
                - To run without calibrations:
                    ▢ specify "calibration": false in the analysis_configs.json file
            (S) bias_frames
                ⃝ bias frames will be placed here if you don't place them here
                ⃝ master bias frame will be created and placed here
            (S) dark_frames
                ⃝ dark frames will be placed here if you don't place them here
                ⃝ master dark frame will be created and placed here
            (S) flat_frames
                ⃝ flat frames will be placed here if you don't place them here
                ⃝ master flat frame will be created and placed here
        (I) red_frames
             ⃝ reduced science frames will be placed here
        (I) file_outputs
             ⃝ any text files created for analysis will be placed here
                - all text files will be space separated
                - use pd.read_csv('file.txt',sep=' ') to read in output files
            (S) logs
                ⃝ log files from each run will be placed here
            (S) data_sheets
                ⃝ data sheets from each run will be placed here
----------------------------------------------------------------------------------------------------------
Creates:
    1) Plots and whatnot
    2) Log file containing the configurations and pertinent operations performed during the run
----------------------------------------------------------------------------------------------------------
"""
#--------------------------------------------------------------------------------------------------------#
#                                          Packages and whatnot                                          #
#--------------------------------------------------------------------------------------------------------#
import os
import shutil
import warnings
import pandas as pd
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot
#.......................................................#
#           Things I will probably use later            #
#.......................................................#
# import ccdproc
# from astropy import units as u
# from astropy.nddata import CCDData
# from astropy.io import fits
# from photutils import CircularAperture
# from photutils import aperture_photometry
# from photutils import CircularAnnulus
# import scipy.optimize as opt
# import scipy.signal
from time import sleep   # ===========================================================   this used for testing (REMOVE LATER)

#--------------------------------------------------------------------------------------------------------#
#                                   Functions and Classes and whatnot                                    #
#--------------------------------------------------------------------------------------------------------#
class frame(object):
    """
    Object to store information about each frame in so the file doesn't have to be open to access some
    of the header info that may be pertinent.  Add to this class as you please.
    """
    def __init__(self,name,path,frame_type):
        self.name = name
        self.path = path
        self.frame_type = frame_type

def check_directories():
    """
    Checks for and creates the directories and subdirectories that will be used throughout the rest of
    the code.

    -This will also remove the files that are not necessary to run HPU_Reduce if they still exist.
     This includes the README.md file, so you will want to view this on the github page as it will be
     easier to see anyway.  If you would like to modify the file structure, you can do so here.

    -This also assumes you have cloned the github repository into the directory that you wish to
     run everything in.  If you accidentally clone it somewhere else, you can move the files
     and directories or add an additional path to where the data are.
    -----------------------------------------------------------------------------------------------------
    Takes in:
        Nothin
    -----------------------------------------------------------------------------------------------------
    Creates the following directories:
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
    -----------------------------------------------------------------------------------------------------
    Removes the following files if they exist:
         ⃝ logo.png
         ⃝ file_tree.png
         ⃝ README.md
         ⃝ LICENSE
    -----------------------------------------------------------------------------------------------------
    Outputs:
        A dictionary containing all of the directories and their respective paths
    -----------------------------------------------------------------------------------------------------
    """
    # ------------------------  Remove specified files  ------------------------ #
    rm_files = ["logo.png","file_tree.png","README.md","LICENSE"]

    for file in rm_files:
        if(os.path.exists(file)==True):
            os.remove(file)

    # ------------------------  Create specified directories  ------------------------ #
    int_dirs = ["raw_frames","cal_frames","red_frames","file_outputs","plots"]
    cal_dirs = ["bias_frames","dark_frames","flat_frames"]
    out_dirs = ["logs","data_sheets"]

    all_dirs = int_dirs+cal_dirs+out_dirs
    all_paths = []

    for int_dir in int_dirs:
        if not os.path.exists(os.path.join(".",int_dir)):
            os.makedirs(int_dir)
        all_paths.append(os.path.join(".",int_dir))
    for cal_dir in cal_dirs:
        if not os.path.exists(os.path.join(".","cal_frames",cal_dir)):
            os.makedirs(os.path.join(".","cal_frames",cal_dir))
        all_paths.append(os.path.join(".","cal_frames",cal_dir))
    for out_dir in out_dirs:
        if not os.path.exists(os.path.join(".","file_outputs",out_dir)):
            os.makedirs(os.path.join(".","file_outputs",out_dir))
        all_paths.append(os.path.join(".","file_outputs",out_dir))

    return dict(zip(all_dirs,all_paths))

def sort_frames(cal_paths):
    """
    Sorts all of the science and calibration frames that match the file format for the telescope used
    (given by telescope_info.json).
    -This function assumes that the reduced science frames are using the
     same image type created later in the code ("reduced"), so if you calibrate the images somewhere else,
     make sure to edit the header of those files to match this so they don't get sorted into the same
     directory as the raw science frames.
    -This function will give priority to NEW frames with the same name.  Therefore, if you drop 10 files
     in that have already been taken, you can drop the whole series in at the end and the function will
     remove the original 10 files and replace them with the ones from the series that have the same name.
     This means that if for some reason you screw up the name of a file or its header, the code will
     probably break somewhere down the line.
    -----------------------------------------------------------------------------------------------------
    Takes in:
        cal_paths: dictionary containing the file types that are telescope dependent and paths that link
                   them to their respective directories
    -----------------------------------------------------------------------------------------------------
    Outputs:
        A print statement that lets you know the files were sorted
    -----------------------------------------------------------------------------------------------------
    """
    for root, dirs, files in os.walk(".",topdown=False):
        for file in files:
            if(file.endswith(file_key)):
                f = fits.open(os.path.join(root,file))
                if(f[0].header[image_typ]!="reduced"):
                    if(os.path.join(root,file)==os.path.join(cal_paths[f[0].header[image_typ]],file)):
                        f.close()
                    else:
                        temp_frame = frame(file,os.path.join(cal_paths[f[0].header[image_typ]],file),f[0].header[image_typ])
                        if not(os.path.exists(os.path.join(cal_paths[f[0].header[image_typ]],file))):
                            f.close()
                            shutil.move(os.path.join(root,file),cal_paths[temp_frame.frame_type])
                        else:
                            os.remove(os.path.join(cal_paths[f[0].header[image_typ]],file))
                            f.close()
                            shutil.move(os.path.join(root,file),cal_paths[temp_frame.frame_type])
                else:
                    f.close()
    return print("All files sorted into their respective directories","\n")

def create_log(log_dict):
    """
    Creates a log file for each run with the current configurations specified in the analysis_configs
    as well as any other operations that might be pertinent to track
    -----------------------------------------------------------------------------------------------------
    Takes in:
        log_dict: A dictionary containing the configurations and operations performed during the run
    -----------------------------------------------------------------------------------------------------
    Outputs:
        run_#_log.txt: space separated log file containing the configurations and operations
                       performed during the run
    -----------------------------------------------------------------------------------------------------
    """
    log_num = 1
    while(os.path.exists(f'logs/run_{log_num}_log.txt')==True):
        log_num+=1
    log_file = pd.DataFrame(log_dict)
    log_file.to_csv(f'logs/run_{log_num}_log.txt',sep=' ',index=False)

    return print(f'Created log for run_{log_num}')

#--------------------------------------------------------------------------------------------------------#
#                                  Main code and variables and whatnot                                   #
#--------------------------------------------------------------------------------------------------------#
# ignore those pesky warnings if we are re-running the code and re-reducing the data
warnings.filterwarnings('ignore', message='Overwriting existing file')

#.......................................................#
#             Things that are likely done               #
#.......................................................#
config_params = pd.read_json("analysis_configs.json")
config_params = config_params["analysis_configs"]
telescope_params = pd.read_json("telescope_info.json")
telescope_params = telescope_params[config_params.loc["telescope"]]

dir_paths = check_directories()
file_key = telescope_params.loc["file_format"]
image_typ = telescope_params.loc["image_type_name"]

if(config_params.loc["flats_used"]=="dome"):
    cal_keys = ["object_frame_name","bias_frame_name","dark_frame_name","dome_flat_frame_name"]
    cal_dirs = ["raw_frames","bias_frames","dark_frames","flat_frames"]
elif(config_params.loc["flats_used"]=="sky"):
    cal_keys = ["object_frame_name","bias_frame_name","dark_frame_name","sky_flat_frame_name"]
    cal_dirs = ["raw_frames","bias_frames","dark_frames","flat_frames"]
else:
    cal_keys = ["object_frame_name","bias_frame_name","dark_frame_name","dome_flat_frame_name","sky_flat_frame_name"]
    cal_dirs = ["raw_frames","bias_frames","dark_frames","flat_frames","flat_frames"]
cal_paths = []
for i, key in enumerate(cal_keys):
    cal_keys[i] = telescope_params.loc[key]
    cal_paths.append(dir_paths[cal_dirs[i]])

cal_paths = dict(zip(cal_keys,cal_paths))
sort_frames(cal_paths)

#.......................................................#
#         Things that probably need tweaking            #
#.......................................................#
place_holder = np.arange(0,20,1)
calibrating = tqdm(place_holder,desc="Calibrating Raw Frames")
extracting_photometry = tqdm(place_holder,desc="Extracting Photometry")


run_configs = []
run_values = []

for val in config_params.index.values:
    run_configs.append(val)
for val in config_params:
    run_values.append(val)

log_dict = {"run_configs:": run_configs, "run_values": run_values}

for i in reducing:
    z=2+i
    sleep(0.5)


#--------------------------------------------------------------------------------------------------------#
# general comment header setup #
#--------------------------------------------------------------------------------------------------------#
