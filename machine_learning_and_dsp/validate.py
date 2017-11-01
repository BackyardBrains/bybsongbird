import os
from functools import partial

import pathos.multiprocessing as mp
from pathos.multiprocessing import Pool

from clean_and_test import clean_and_test, test_params
from train_model import train_model


def train_and_verify(directory, classifierType, birds, mtStep, mtWin, stStep, stWin):
    train_rootdir = os.path.join(directory, 'Training')
    test_rootdir = os.path.join(directory, 'Testing')
    train_dirs = test_params(train_rootdir, birds)
    model = 'x'.join([classifierType, str(mtStep), str(mtWin), str(stStep), str(stWin)])
    train_model(modelName=model, mtWin=mtWin, mtStep=mtStep, stWin=stWin, stStep=stStep, classifierType=classifierType,
                list_of_dirs=train_dirs)
    clean_and_test(directory=test_rootdir, classifierType=classifierType, no_sanitize=True, skip_clean=True,
                   show_graphs=False, model_file=model, birds=birds, verbose=False, num_threads=0)


if __name__ == '__main__':
    birds = ['bluejay_all', 'cardinal_song', 'chickadee_song', 'crow_all', 'goldfinch_song', 'robin_song',
             'sparrow_song', 'titmouse_song']
    directory = '/run/media/zach/untitled/ML_Recordings/xeno-canto'
    classifierType = ['gradientboosting', 'svm']
    mtStep = [0.1, 0.2]
    mtWin = [0.2, 0.4]
    stStep = [0.01, 0.02]
    stWin = [0.02, 0.04]

    verifier = partial(target=train_and_verify, directory=directory, birds=birds)

    pros = Pool(mp.cpu_count())
    pros.map(verifier, classifierType, mtStep, mtWin, stStep, stWin)
