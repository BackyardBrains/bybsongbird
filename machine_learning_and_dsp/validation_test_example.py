
#! python

#An example validation script
import matplotlib
matplotlib.use('Pdf')
import os
from validate import validate



if __name__ == '__main__':
    #See pyAudioAnalysis docs for info on these parameters, this script will test alll reasonable combonations of the parameters in 
    #these lists
    directory = os.getcwd()
    classifierType = ['svm']
    mtStep = [1.0, 0.5, 0.1]
    mtWin = [1.0, 0.5, 0.1]
    stStep = [0.1, 0.05, 0.01]
    stWin = [0.1, 0.05, 0.01]
    #The number of seperate processes to run in paralel (not counting the master), 
    #if using flux I reccomend this be the same or slightly less than your cpu count
    num_threads = 18
    validate(directory=directory, classifierType=classifierType, mtStep=mtStep, mtWin=mtWin, stStep=stStep, stWin=stWin,
             num_threads=num_threads, debug=False, skip_clean=True)
    #if skip_clean is set to false the entire training and testing sets will be processed for noise reduction, this takes a long time 
    #and only needs to be done once. If using flux you probably want to do this part in advance on your own p.c. and copy only the 
    #preprocessed files into your school account
    
    #debug should normally be false unless your testing changes that you made to something as some files can be unprocessable due
    # to problems with the audio, etc. This will ignore most errors though, so if you make any changes to validate.py or anything that
    # it calls from, just make sure you test it properly or you could end up training on an incomplete dataset.
