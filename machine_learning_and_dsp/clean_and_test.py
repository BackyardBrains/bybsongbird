#! python
import matplotlib

#matplotlib.use("Pdf")
#
from matplotlib import pyplot as plt

import getopt
import os
import sys
import time

from numpy import mean

from noise_removal import noiseCleaner
from sanitize_filenames import sanatize_filenames
from test_model import tester, basic_roc_plot


# This function will take the directory name(dir) and the bird names (categories) and return a list of folder paths of the form dir/bird_name
def test_params(dir, categories):
    test_dirs = []
    for cat in categories:
        test_dirs.append(os.path.join(dir, cat, '_'.join([cat, 'clean'])))

    return test_dirs


# When given a directory with folders "Testing" and "Training" containing test-set wav files and training-set wav files respectively
#Will "clean" (run preprosecssing) on all wav_files then runs a full validation test across selection thresholds 0.0 through 0.9 and generates an ROC curve
def clean_and_test(directory, model_file, classifierType, birds, verbose, skip_clean, no_sanitize,
                   show_graphs=True):
    if not len(birds):
        raise Exception("Must specify at least one folder/category to test!")

    start_time = time.clock()

    # birds = ['bluejay_all', 'cardinal_song',
    # 'chickadee_song', 'crow_all', 'goldfinch_song', 'robin_song',
    # 'sparrow_song', 'titmouse_song']

    test_dirs = test_params(directory, birds)

    try:
        if not no_sanitize:
            sanatize_filenames(directory, verbose=verbose)
        if not skip_clean:
            for dir in test_dirs:
                rootdir, subdir = os.path.split(dir)
                cleaner = noiseCleaner(verbose=verbose, num_threads=0)
                cleaner.noise_removal_dir(rootdir)
        model_dir, model_name = os.path.split(model_file)
        print ''
        thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        t1 = tester(test_dirs=test_dirs, model_dir=model_dir, modelName=model_name, verbose=verbose,
                    classifierType=classifierType)
        tests = []

        for t in thresholds:
            tests.append(t1.test_model(t))

        num_classes = len(birds)
        per_class_fpr = [[] for a in xrange(num_classes)]
        per_class_tpr = [[] for a in xrange(num_classes)]
        micro_average_fpr = []
        micro_average_tpr = []
        for v in tests:
            micro_average_fpr.append(mean([1 - v[f].spec for f in xrange(num_classes)]))
            micro_average_tpr.append(mean([v[f].sens for f in xrange(num_classes)]))

            for q in xrange(0, num_classes):
                per_class_fpr[q].append(1 - v[q].spec)
                per_class_tpr[q].append(v[q].sens)

        auc_scores = []
        for g in xrange(num_classes):
            auc_scores.append(basic_roc_plot(per_class_fpr[g], per_class_tpr[g], birds[g], show_graph=show_graphs))

        macro_average_auc = mean(auc_scores)

        micro_average_auc = basic_roc_plot(micro_average_fpr, micro_average_tpr, "Micro-average",
                                           show_graph=show_graphs, save_graph=True, filename=model_file)
        plt.clf()
        print "AUC for %s is %s" % ("Macro-average", macro_average_auc)
    except Exception:
        # send_notification("Clean and test process failed.")
        raise
    else:
        #send_notification("Clean and test finished successfully.")
        print "Total time elapsed: ", time.clock() - start_time, " seconds."
        return [micro_average_fpr, micro_average_tpr, micro_average_auc, tests]


if __name__ == '__main__':

    directory = os.getcwd()
    classifierType = 'svm'
    birds = []
    verbose = False
    model_file = os.path.join(directory, 'model')
    skip_clean = False
    no_sanitize = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:m:c:b:vsn",
                                   ["dir=", "model=", "classifier=", "bird=", "verbose", "skip-clean", "no-sanitize", ])
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
        elif opt in ("-b", "--bird"):
            birds.append(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-s", "--skip-clean"):
            skip_clean = True
        elif opt in ("-n", "--no-sanitize"):
            no_sanitize = True
        else:
            assert False, "unhandled option"

    if not os.path.isfile(model_file):
        raise Exception("Model file:" + model_file + " not found!")

    if classifierType not in ('knn', 'svm', 'gradientboosting', 'randomforest', 'extratrees'):
        raise Exception(classifierType + " is not a valid model type!")

    clean_and_test(directory, model_file, classifierType, birds, verbose=verbose, skip_clean=skip_clean,
                   no_sanitize=no_sanitize)
