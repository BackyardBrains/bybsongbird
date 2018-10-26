from noise_removal import noiseCleaner 
import os 
from sanitize_filenames import sanatize_filenames 

directory = os.getcwd()
dirs=[]
dirs.append(os.path.join(directory,'Training'))
#dirs.append(os.path.join(directory,'Testing'))
dirs.append(os.path.join(directory,'Validation'))
for d in dirs:
	print d	
#	sanatize_filenames(d,verbose=True)
	cleaner = noiseCleaner()
	cleaner.noise_removal_dir(d)

