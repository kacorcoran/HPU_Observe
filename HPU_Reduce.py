"""
HPU_Reduce --- The Helpful Photometric Uranoscopy Reduction Code
Kyle Corcoran - University of Virginia
kac8aj@virginia.edu
2020

Prerequisites:
    1) Written in Python 3 (may work in 2.7 - will check later)
    2) Installation of the following packages (assuming they are not already installed):
        ⃝ tqdm
        ⃝ astropy
        ⃝ ccdproc
        ⃝

File Structure Setup:
    1) Create a directory in your desired location and place HPU_Reduce.py there
    2) Create a subdirectory called raw_frames and place your science frames here
        ⃝ This assumes you have removed images which are not usable (e.g., smearing from telescope bump)
    3) Create a subdirectory called cal_frames and place your calibration frames here
        ⃝ Leave this directory empty if you have not taken cals yet
        ⃝ To run without


creates /reduced/cals/ and /reduced/data/
"""

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
