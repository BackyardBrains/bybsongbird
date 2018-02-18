#! python

import cPickle
import itertools
import os
from copy import deepcopy
from functools import partial

import pathos.multiprocessing as mp
from pathos.multiprocessing import Pool

from clean_and_test import clean_and_test, test_params
from train_model import train_model


#You should never need to call this function directly as validate() handles it automatically
#Trains and tests models using parameters outlined in the example usage file
#parameters is a list of you params in the correct order
#birds is your classes
#debug prints extra info
#skip_clean skips audio preprocessing, which only needs to be done once
def train_and_verify(parameters, directory, birds, debug=False, skip_clean=True):
    try:
        os.chdir(directory)
        classifierType = parameters[0]
        mtStep = parameters[1]
        mtWin = parameters[2]
        stStep = parameters[3]
        stWin = parameters[4]
        train_rootdir = os.path.join(directory, 'Training')
        test_rootdir = os.path.join(directory, 'Testing')
        train_dirs = test_params(train_rootdir, birds)
        model = 'x'.join([classifierType, str(mtStep), str(mtWin), str(stStep), str(stWin)])
        model_path = os.path.join(os.getcwd(), model)
        if not os.path.exists(model):
            train_model(modelName=model, mtWin=mtWin, mtStep=mtStep, stWin=stWin, stStep=stStep,
                        classifierType=classifierType,
                        list_of_dirs=train_dirs)
        png_path = '.'.join([model_path, 'png'])
        stats_path = '.'.join([model_path, 'stats'])
        if not os.path.exists(png_path) and not os.path.exists(stats_path):
            stats = clean_and_test(directory=test_rootdir, classifierType=classifierType, no_sanitize=True,
                                   skip_clean=skip_clean,
                                   show_graphs=False, model_file=model_path, birds=birds, verbose=False)
            with open(stats_path, 'w') as stats_file:
                cPickle.dump(stats, stats_file)
    except:
        if debug:
            raise
        else:
            return


#Validates models of different parameter sets automatically using your training and testing sets
#see validation_example.py or songbird doc for more info
#Model files will automatically be named based on their parameters
#Automatically saves all graphs as pngs: see test_model.py for more info
#train_and_verify will automatically "pickle" all the given stats returned by test_model to model_file.stats
#this means it saves the python object to a file that can be re-imported directly as a python object later on
#see test_model for more info about stats and lookup pickle for more info about pickling in Python
def validate(directory, classifierType, mtStep, mtWin, stStep, stWin, num_threads=mp.cpu_count()):

    for root, dirs, files in os.walk(os.path.join(directory, 'Training')):
        birds = dirs
        break

    parameters = list(itertools.product(classifierType, mtStep, mtWin, stStep, stWin))

    # Gets rid of invalid sets of parameters
    parameters_temp = deepcopy(parameters)
    for p in parameters:
        if p[1] > p[2] or p[3] > p[4] or p[4] >= p[2]:
            parameters_temp.remove(p)

    parameters = parameters_temp
    verifier = partial(train_and_verify, directory=directory, birds=birds)

    pros = Pool(num_threads)
    pros.map(verifier, parameters)
