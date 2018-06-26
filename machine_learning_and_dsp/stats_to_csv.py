#! python

#Functions in this file can be used to create a csv file containing the top 20 AUC scores for the roc curves of the models tested
#by drawing from model_file.stats for every model in the directory 
#this can be used to create a graph in excel
#see validate.py and test_model.py for info on this

import cPickle
import csv
import os

from sklearn import metrics


def model_rank_pass1(A):
    return A[6]


def model_rank_pass2(A):
    return A[5]


def table_sort(table):
    table.sort(key=model_rank_pass1, reverse=True)
    table.sort(key=model_rank_pass2, reverse=True)
    return table

def stats_to_csv(directory):
    os.chdir(directory)
    root, foldername = os.path.split(directory)
    outfile_name = '.'.join([foldername, 'csv'])
    with open(outfile_name, 'w') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Model', 'mtStep', 'mtWin', 'stStep', 'stWin', 'Micro-Average AUC', 'Worst-Case AUC'])
    csv_table = []
    for file in os.listdir(os.getcwd()):
        if file.endswith('.stats'):
            with open(file, 'r') as stats_file:
                micro_average_fpr, micro_average_tpr, micro_average_auc, tests = cPickle.load(stats_file)
            num_classes = len(tests[0])
            model_name = file.rsplit('.stats')[0]
            csv_entry = model_name.split('x')
            per_class_fpr = [[] for a in xrange(num_classes)]
            per_class_tpr = [[] for a in xrange(num_classes)]
            for v in tests:
                for q in xrange(0, num_classes):
                    per_class_fpr[q].append(1 - v[q].spec)
                    per_class_tpr[q].append(v[q].sens)
            auc_scores = []
            for g in xrange(num_classes):
                auc_scores.append(metrics.auc(per_class_fpr[g], per_class_tpr[g]))
            worst_case_auc = min(auc_scores)
            csv_entry += [micro_average_auc, worst_case_auc]
            csv_table.append(csv_entry)
    csv_table = table_sort(csv_table)
    csv_table = csv_table[0:20]
    for row in csv_table:
        with open(outfile_name, 'a') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(row)
