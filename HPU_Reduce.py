"""
HPU_Reduce --- The Helpful Photometric Uranoscopy Reduction and Analysis Code
Kyle Corcoran - University of Virginia
kac8aj@virginia.edu
2020
----------------------------------------------------------------------------------------------------------
Prerequisites:
    1) Written in Python 3 (may work in 2.7 - will check later)
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
    ....................................................................................
    Key:
    (T) = Top directory   (I) = Middle/Intermediate directory   (S) = Bottom directory
    ....................................................................................
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
#.......................................................#
#             Things that are likely done               #
#.......................................................#
param_configs = []
run_values = []
log_dict = {"param_configs:": param_configs, "run_values": run_values}
#.......................................................#
#              Things that need tweaking                #
#.......................................................#
place_holder = np.arange(0,20,1)
calibrating = tqdm(place_holder,desc="Calibrating Science Frames")
extracting_photometry = tqdm(place_holder,desc="Extracting Photometry")


for i in reducing:
    z=2+i
    sleep(0.5)


#--------------------------------------------------------------------------------------------------------#
# general comment header setup #
#--------------------------------------------------------------------------------------------------------#
