#! python
# -*- coding: utf-8 -*-

#This file contains functions to test a model and get stats to validate it

import cPickle
import glob
import os
import time

import matplotlib.pyplot as plt
import numpy as np
from numpy import mean
from pyAudioAnalysis import audioTrainTest as aT
from sklearn import metrics


#processes raw data into stats
def find_stats(stats_matrix):
    stats = [class_stats(q) for q in stats_matrix]

    marker = 0
    for obj in stats:
        obj.stats_eval()
        print "F-score for class %s is %s" % (marker, obj.f_score())
        marker = marker + 1

    #Hopefully working paralellization for this part:
    #pros = Pool(num_threads)
    #pros.map(class_stats.stats_eval, stats)

    # Find micro-average F1
    micro_prec = do_division(sum([i.true_pos for i in stats]), sum([i.true_pos + i.false_pos for i in stats]))
    micro_recall = do_division(sum([i.true_pos for i in stats]), sum([i.true_pos + i.false_neg for i in stats]))
    micro_f1 = f_score(micro_prec, micro_recall)
    print "Micro-averaged F1 is %s \n" % micro_f1

    # Find macro-average F1
    macro_prec = mean([i.prec for i in stats])
    macro_recall = mean([i.recall for i in stats])
    macro_f1 = f_score(macro_prec, macro_recall)
    print "Macro-averaged F1 is %s \n" % macro_f1

    return stats


#Calculate and f-score
#research stats for validating ml models and f-scores for more info
def f_score(prec, recall, Beta=1):
    fscore = do_division((1 + Beta ** 2) * (prec * recall), (Beta ** 2 * prec + recall))
    return fscore

#Stats object
#contains true positives, false positives, true negatives, false positives, and true negatives
#contatins accuracy, sensitivity (recall), and specificity
#Research stats for ml to find out more about these
class class_stats:
    def __init__(self, stats_row):
        self.stats_row = stats_row

    def stats_eval(self):
        stats_row = self.stats_row

        true_pos = stats_row[0]
        false_pos = stats_row[1]
        false_neg = stats_row[2]
        true_neg = stats_row[3]


        full_matrix_sum = sum(stats_row)

        accu = do_division((true_pos + true_neg), full_matrix_sum)
        sens = do_division(true_pos, (true_pos + false_neg))
        spec = do_division(true_neg, (true_neg + false_pos))

        prec = do_division(true_pos, (true_pos + false_pos))
        recall = sens

        self.true_pos = true_pos
        self.true_neg = true_neg
        self.false_pos = false_pos
        self.false_neg = false_neg

        self.accu = accu
        self.sens = sens
        self.spec = spec
        self.prec = prec
        self.recall = recall

    def f_score(self, Beta=1):
        prec = self.prec
        recall = self.recall
        fscore = do_division((1 + Beta**2) * (prec * recall), (Beta**2 * prec + recall))
        return fscore



#This is just a workaround for divide by 0 error
def do_division(a, b):
    if a == 0 and b == 0:
        return 0.0
    else:
        return float(a) / float(b)

#This is just a workaround for problems with Python's automatic pass-by-reference
#See the stackoverlow page if you want more info
def unshared_copy(inList):
    #https://stackoverflow.com/questions/1601269/how-to-make-a-completely-unshared-copy-of-a-complicated-list-deep-copy-is-not
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList


#Tester class
#test directories are the directories for each class in your "Testing" folder
#model_dir is the directory containing your model files, and modelName is the name of the model
#classifierType is the ml algorithm that you used to train the classifier, see pyAudioAnalysis and scikit-learn docs for more info
#verbose prints info on each model as it is tested
class tester:
    def __init__(self, test_dirs, model_dir=os.getcwd(), modelName='THISONEHSDLKGDSLKGJSLDKJGLKD', classifierType='gradientboosting',
                 verbose=False):
        self.test_dirs = test_dirs
        self.model_dir = model_dir
        self.modelName = modelName
        self.classifierType = classifierType
        self.verbose = verbose

    #Tests a single model
    #A wav file is treated as being identified as a given class if the probability returned by the classifier is > level
    #So for example if level==0.3 and file1.wav returns a 0.4 probability that it is a chickadee and a 0.5 probability that it
    #is a goldfinch then the tester will treat this as a positive id for both chickadee and goldfinch
    #if the actual identity of the file is a goldfinch then this would be considered a true positive for the goldfinch class AND
    #a false positive for the chickadee class
    #The validation script will test the model at all levels from 0.0 to 0.9 in 0.1 increments in order to generate an ROC curve
    #for each class and for the average, which will automatically be saved to a png
    #research ROC curves for more info
    #The function will return all of the generated stats for later processing, see validate.py for more info about this
    def test_model(self, level=0.5):

        test_dirs = self.test_dirs
        model_dir = self.model_dir
        modelName = self.modelName
        classifierType = self.classifierType
        verbose = self.verbose

        start_time = time.clock()

        os.chdir(test_dirs[0])
        for file in glob.glob(u"*.wav"):  # Iterate through each wave file in the directory
            Result, P, classNames = aT.fileClassification(file, os.path.join(model_dir, modelName),
                                                          classifierType)  # Test the file
            break

        if classNames == -1:
            raise Exception("Model file " + os.path.join(model_dir, modelName) + " not found!")

        num_cats = len(classNames)
        temp = []
        for j in xrange(0, num_cats):
            temp.append(0)
        confusion_matrix = []
        for k in xrange(0, num_cats):
            confusion_matrix.append(unshared_copy(temp))

        confidence_above_90 = unshared_copy(temp)
        correct_above_90 = unshared_copy(temp)
        total_num_samples = unshared_copy(temp)
        confidence_corrected_con_matrix = unshared_copy(confusion_matrix)
        stats_matrix = [[0, 0, 0, 0] for x in xrange(0, num_cats)]
        for i in xrange(0, len(test_dirs)):  # Iterate through each test directory
            dir = test_dirs[i]
            os.chdir(dir)
            rootdir, correct_cat = os.path.split(dir)
            for file in glob.glob(u"*.wav"):  # Iterate through each wave file in the directory
                result_pickle = '.'.join([file, modelName])
                if os.path.exists(result_pickle):
                    with open(result_pickle, 'r') as result_file:
                        Result, P, classNames = cPickle.load(result_file)
                else:
                    with open(result_pickle, 'w') as result_file:
                        Result, P, classNames = aT.fileClassification(file, os.path.join(model_dir, modelName),
                                                                      classifierType)  # Test the file
                        cPickle.dump([Result, P, classNames], result_file)

                if verbose:
                    print '\n', file
                    print Result
                    print classNames
                    print P, '\n'


                threshold = level

                for cls in xrange(0, len(P)):
                    if P[cls] > threshold:
                        if unicode(correct_cat) == unicode(classNames[cls]):
                            # True Positive
                            stats_matrix[cls][0] = stats_matrix[cls][0] + 1
                        else:
                            # False Positive
                            stats_matrix[cls][1] = stats_matrix[cls][1] + 1
                    else:
                        if unicode(correct_cat) == unicode(classNames[cls]):
                            # False Negative
                            stats_matrix[cls][2] = stats_matrix[cls][2] + 1
                        else:
                            # True Negative
                            stats_matrix[cls][3] = stats_matrix[cls][3] + 1

                identified_correctly = (unicode(correct_cat) == unicode(classNames[int(Result)]))
                confidence = max(P)

                indexes = [t for t, x in enumerate(classNames) if unicode(x) == unicode(correct_cat)]
                if not unicode(correct_cat) == u'no_cat':

                    if not len(indexes):
                        raise Exception(correct_cat + "is not a correctly named category for this model!")
                    elif len(indexes) != 1:
                        raise Exception(correct_cat + "matches multiple categories in the model file!")
                    cat_index = indexes[0]
                    total_num_samples[cat_index] += 1
                    confusion_matrix[cat_index][int(Result)] += 1
                    if confidence > level:
                        confidence_corrected_con_matrix[cat_index][int(Result)] += 1
                        confidence_above_90[cat_index] += 1
                        if unicode(correct_cat) == unicode(classNames[int(Result)]):
                            assert (identified_correctly)
                            correct_above_90[cat_index] += 1

        acc_above_90 = map(do_division, correct_above_90, confidence_above_90)
        percent_desicive_samples = map(do_division, confidence_above_90, total_num_samples)

        print '\n', "Agregated Results: ", '\n'
        print classNames
        print "acc above ", level, ": ", acc_above_90
        print "percent samples above ", level, ": ", percent_desicive_samples
        print "total samples tested in each category: ", total_num_samples, '\n'
        print "confusion matrix:"
        aT.printConfusionMatrix(np.array(confusion_matrix), classNames)
        print "\n", "confidence adjusted confustion matrix:"
        aT.printConfusionMatrix(np.array(confidence_corrected_con_matrix), classNames)

        print '\n', "Processed ", sum(total_num_samples), " samples in ", time.clock() - start_time, " seconds."

        stats = find_stats(stats_matrix)

        self.stats = stats
        return stats


#Creates the ROC plot using matplotlib
#Show graph will show the graph on screen automaticlly when it is created
#This will interrupt the process and should be disabled for large tests
#save_graph automatically saves a .png of the graph to filename.png
def basic_roc_plot(fpr, tpr, className, show_graph=True, save_graph=False, filename='graph'):
    #https://stackoverflow.com/questions/25009284/how-to-plot-roc-curve-in-python
    roc_auc = metrics.auc(fpr, tpr)
    print "AUC for %s is %s" % (className, roc_auc)
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='%s = %0.2f' % (className, roc_auc), c=np.random.rand(3, ))
    plt.legend(loc='lower right')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    if save_graph:
        plt.savefig('.'.join([filename, 'png']))
    if show_graph:
        plt.show()
    return roc_auc
