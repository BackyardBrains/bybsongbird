#! python

# This is a command line utility to classify a folder of bird songs
# Will automatically do preprocessing, classify, extract environmental data and insert into the MySQL Database
# -d, --dir : Directory of Files to classify
# -m, --model : Location of the model files created from training
# -c, --classifier : the ml algorithm the model was trained with, will be one of: [gradientboosting (default), svm, randomforest, extratrees, knn]
# -v, --verbose : Print the classifier results of each file to stdout
# -e, --export : Exports the entire sql database to an .sql file
# -r, --run : runs the preprocessing and classifier, it will not run without this flag
# -n, --num-threads : the number of threads to use for classification, by default will use the number of cpus on the system, set this to 0 to debug


import getopt
import os
import sys

import pathos.multiprocessing as mp

from process_and_categorize import classiFier

if __name__ == '__main__':

    directory = os.getcwd()
    classifierType = 'gradientboosting'
    birds = []
    verbose = False
    model_file = os.path.join(directory, 'model')
    export = False
    run = False
    num_threads = mp.cpu_count()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:m:c:vern:",
                                   ["dir=", "model=", "classifier=", "verbose", "export", "run", "num-threads="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--dir"):
            directory = arg
        elif opt in ("-m", "--model"):
            model_file = arg
        elif opt in ("-c", "--classifier"):
            classifierType = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-e", "--export"):
            export = True
        elif opt in ("-r", "--run"):
            run = True
        elif opt in ("-n", "--num-threads"):
            num_threads = int(arg)
        else:
            assert False, "unhandled option"

    if not os.path.isfile(model_file):
        raise Exception("Model file:" + model_file + " not found!")

    if classifierType not in ('knn', 'svm', 'gradientboosting', 'randomforest', 'extratrees', 'mlp'):
        raise Exception(classifierType + " is not a valid model type!")

    classifier0 = classiFier(directory, model_file, classifierType, verbose=verbose, num_threads=num_threads)
    if run:
        classifier0.classify()
    if export:
        classifier0.export()
    if not run and not export:
        sys.stderr.write("No operator flags set: exiting!")
        exit(1)
