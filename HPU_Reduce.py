"""
----------------------------------------------------------------------------------------------------------
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
    I have included some of the same directory creation code here just in case, but, at a minimum,
    the raw_frames directory needs to be made and contain the raw science frames for the code to run.
    (T) = Top directory   (M) = Middle/Intermediate directory   (B) = Bottom directory

    (T) Directory in your desired location where you place HPU_Reduce.py
        (M) raw_frames
             ⃝ place your science frames here
                - This assumes you have removed images which are not usable
                  (e.g., smearing from telescope bump)
        (M) cal_frames
             ⃝ place your calibration frames here
                - Leave this directory empty if you have not taken cals yet
                - To run without
            (B) bias_frames
                ⃝ bias frames will be placed here if you don't place them here
                ⃝ master bias frame will be created and placed here
            (B) dark_frames
                ⃝ dark frames will be placed here if you don't place them here
                ⃝ master dark frame will be created and placed here
            (B) flat_frames
                ⃝ flat frames will be placed here if you don't place them here
                ⃝ master flat frame will be created and placed here
        (M) red_frames
             ⃝ reduced science frames will be placed here
        (M) file_outputs
             ⃝ any text files created for analysis will be placed here
                - all text files will be space separated
                - use pd.read_csv('file.txt', sep=' ', header=0) to read in output files
----------------------------------------------------------------------------------------------------------

creates /reduced/cals/ and /reduced/data/
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot

#-------------------------------------------------------#
#------------    Things I will use later    ------------#
#-------------------------------------------------------#
# import ccdproc
# from astropy import units as u
# from astropy.nddata import CCDData
# from astropy.io import fits

#-------------------------------------------------------#
from time import sleep   # this used for testing (REMOVE LATER)

x = np.arange(0,20,1)
reducing = tqdm(x,desc='Reducing Science Frames')
for i in reducing:
    z=2+i
    sleep(0.5)
