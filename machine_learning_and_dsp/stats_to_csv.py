import cPickle
import csv
import os

from sklearn import metrics


def stats_to_csv(directory):
    os.chdir(directory)
    root, foldername = os.path.split(directory)
    outfile_name = '.'.join([foldername, 'csv'])
    with open(outfile_name, 'w') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Model', 'mtStep', 'mtWin', 'stStep', 'stWin', 'Micro-Average AUC', 'Worst-Case AUC'])
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
            with open(outfile_name, 'a') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(csv_entry)
