import cPickle
import itertools
import os
from copy import deepcopy
from functools import partial

import pathos.multiprocessing as mp
from pathos.multiprocessing import Pool
from noise_removal import noiseCleaner
from clean_and_test import clean_and_test, test_params
from train_model import train_model


def train_and_verify(parameters, directory, birds, debug=False):
    try:
        os.chdir(directory)
        classifierType = parameters[0]
        mtStep = parameters[1]
        mtWin = parameters[2]
        stStep = parameters[3]
        stWin = parameters[4]
        train_rootdir = os.path.join(directory, 'Training')
        test_rootdir = os.path.join(directory, 'Validation')
        train_dirs = test_params(train_rootdir, birds)
        model = 'x'.join([classifierType, str(mtStep), str(mtWin), str(stStep), str(stWin)])
        model_path = os.path.join(os.getcwd(), model)
        if not os.path.exists(model):
            train_model(list_of_dirs=train_dirs, mtWin=mtWin, mtStep=mtStep, stWin=stWin, stStep=stStep,
                        classifierType=classifierType, modelName=model)
        png_path = '.'.join([model_path, 'png'])
        stats_path = '.'.join([model_path, 'stats'])
        if not os.path.exists(png_path) and not os.path.exists(stats_path):
            stats = clean_and_test(directory=test_rootdir, classifierType=classifierType, no_sanitize=True,
                                   skip_clean=True,
                                   show_graphs=False, model_file=model_path, birds=birds, verbose=False)
            with open(stats_path, 'w') as stats_file:
                cPickle.dump(stats, stats_file)
    except:
        if debug:
            raise
        else:
            return


def validate(directory, classifierType, mtStep, mtWin, stStep, stWin, num_threads=mp.cpu_count()):

    for root, dirs, files in os.walk(os.path.join(directory, 'Training')):
	birds = dirs
        break
    directory = directory + 'Training'
    parameters = list(itertools.product(classifierType, mtStep, mtWin, stStep, stWin))
     #Gets rid of invalid sets of parameters
    parameters_temp = deepcopy(parameters)
    for p in parameters:
        if p[1] > p[2] or p[3] > p[4] or p[4] >= p[2]:
           parameters_temp.remove(p)

    parameters = parameters_temp 
    verifier = partial(train_and_verify, directory=directory, birds=birds)

    pros = Pool(num_threads)
    pros.map(verifier, parameters)
