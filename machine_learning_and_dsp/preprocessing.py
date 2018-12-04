from noise_removal import noiseCleaner 
import os 
from sanitize_filenames import sanatize_filenames 

directory = os.getcwd()
train_dir = os.path.join(directory,'Data')
cleaner = noiseCleaner()
cleaner.noise_removal_dir(directory)

