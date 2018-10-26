from validate import validate
import os 

if __name__ == '__main__':

#    directory = '/home/bybsongbird/machine_learning_and_dsp/'
    directory = os.getcwd()
    classifierType = ['gradientboosting']
    mtStep =[0.5, 0.1]
    mtWin = [1.0, 0.5]
    stStep =[0.05, 0.01]
    stWin = [0.1, 0.05]
    num_threads = 16
    validate(directory=directory, classifierType=classifierType, mtStep=mtStep, mtWin=mtWin, stStep=stStep, stWin=stWin,
             num_threads=num_threads)
