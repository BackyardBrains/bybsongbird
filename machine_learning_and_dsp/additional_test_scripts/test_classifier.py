from process_and_categorize import classiFier
import os 
from pyAudioAnalysis import audioTrainTest as aT
import time

start_time = time.time()
root_dir = os.getcwd()
test_dir = os.path.join(root_dir,'Testing','American_Goldfinch','American_Goldfinch_clean')
model_name = 'gradientboostingx0.5x0.5x0.05x0.05'
#model_name = 'randomforestx0.5x1.0x0.01x0.01'
model_file = os.path.join(root_dir,'model_file_9birds',model_name)
classifierType = 'gradientboosting'
directory = test_dir


#birds_dir  = []
#for root, dirs, files in os.walk(test_dir):
#    birds_dir = dirs
#    break

#print birds_dir

#for bird in birds_dir:
#	print 'now classifying files from:'
#	print bird
#	directory = os.path.join(test_dir,bird)
#	classifier0 = classiFier(directory, model_file, classifierType, verbose=True, num_threads=0)
#	classifier0.classify()

for file in os.listdir(directory):
	    file = os.path.join(directory,file)
	    Result, P, classNames = aT.fileClassification(file, model_file, classifierType)
            print file
            print Result
            print classNames
            print P, '\n'

print time.time() - start_time




