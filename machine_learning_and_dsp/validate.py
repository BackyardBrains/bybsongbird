import itertools
import os
from functools import partial

from clean_and_test import clean_and_test, test_params
from train_model import train_model


def train_and_verify(parameters, directory, birds):
    classifierType = parameters[0]
    mtStep = parameters[1]
    mtWin = parameters[2]
    stStep = parameters[3]
    stWin = parameters[4]
    train_rootdir = os.path.join(directory, 'Training')
    test_rootdir = os.path.join(directory, 'Testing')
    train_dirs = test_params(train_rootdir, birds)
    model = 'x'.join([classifierType, str(mtStep), str(mtWin), str(stStep), str(stWin)])
    if not os.path.exists(model):
        train_model(modelName=model, mtWin=mtWin, mtStep=mtStep, stWin=stWin, stStep=stStep,
                    classifierType=classifierType,
                    list_of_dirs=train_dirs)
    clean_and_test(directory=test_rootdir, classifierType=classifierType, no_sanitize=True, skip_clean=True,
                   show_graphs=False, model_file=os.path.join(os.getcwd(), model), birds=birds, verbose=False)


if __name__ == '__main__':
    birds = ['bluejay_all', 'cardinal_song', 'chickadee_song', 'crow_all', 'goldfinch_song', 'robin_song',
             'sparrow_song', 'titmouse_song']
    directory = '/run/media/zach/untitled/ML_Recordings/xeno-canto'
    classifierType = ['gradientboosting']
    mtStep = [0.2]
    mtWin = [0.2]
    stStep = [0.02]
    stWin = [0.02]

    parameters = list(itertools.product(classifierType, mtStep, mtWin, stStep, stWin))

    verifier = partial(train_and_verify, directory=directory, birds=birds)

    # pros = Pool(mp.cpu_count())
    # pros.map(verifier, parameters)
    for params in parameters:
        verifier(params)
