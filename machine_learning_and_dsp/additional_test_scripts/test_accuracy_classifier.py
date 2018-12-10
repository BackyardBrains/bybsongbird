import pandas as pd
import os
from pyAudioAnalysis import audioTrainTest as aT
import itertools
from copy import deepcopy
import glob
import pickle

def test_models(model_dir,classifiertype,param):
    model_file = 'x'.join([classifiertype,str(param[0]),str(param[1]),str(param[2]),str(param[3])])
    return os.path.join(model_dir,model_file)

def test_params(dir, categories):
    test_dirs = []
    for cat in categories:
        test_dirs.append(os.path.join(dir, cat, '_'.join([cat, 'clean'])))

    return test_dirs

def save_result(my_dict):
	f = open("accuracy.pkl","wb")
	pickle.dump(my_dict,f)
	f.close() 


root_dir = os.getcwd()
test_dir = os.path.join(root_dir, 'Testing')
classifierType = 'gradientboosting'
model_dir  = os.path.join(root_dir, 'models')
mtStep = [1.0, 0.5, 0.1]
mtWin = [1.0, 0.5, 0.1]
stStep = [0.1, 0.05, 0.01]
stWin = [0.1, 0.05, 0.01]

parameters = list(itertools.product(mtStep, mtWin, stStep, stWin))
parameters_temp = deepcopy(parameters)
for p in parameters:
	if p[0] > p[1] or p[2] > p[3] or p[3] >= p[1]:
        	parameters_temp.remove(p)

parameters = parameters_temp 

model_files = list(map(lambda params: test_models(model_dir,classifierType,params) , parameters))
model_files_temp = deepcopy(model_files)
for model_file in model_files:
	if not os.path.isfile(model_file):
   		 model_files_temp.remove(model_file)
model_files = model_files_temp

birds  = []
for root, dirs, files in os.walk(test_dir):
    birds = dirs
    break

test_dirs = test_params(test_dir, birds)
accuracy_dict = {}
accuracy_dict['model'] = []
accuracy_dict['accuracy'] = []
for model_file in model_files:
	_ , model = os.path.split(model_file)
	accuracy_dict['model'].append(model)
	num = 0
	correct_classified = 0
	print model
	for bird in test_dirs:
	    _,correct_cat = os.path.split(bird)
	    print 'now classifying files from:'
	    print correct_cat
	    for file in os.listdir(bird):
		num_bird = 0
		correct_bird = 0
		if file.endswith('.wav') or file.endswith('.WAV'):
			file = os.path.join(bird,file)
			num += 1
			Result, P, classNames = aT.fileClassification(file, model_file, classifierType)
			print Result
			print classNames
			if unicode(correct_cat) == unicode(classNames[int(Result)]):
				correct_classified += 1
				correct_bird += 1
            print num_bird
            print correct_bird

	print correct_classified
	print 'finished processing ', num , ' samples'
	accuracy = (float(correct_classified)/float(num))*100
	print accuracy
	accuracy_dict['accuracy'].append(accuracy)


accuracy_df = pd.DataFrame(accuracy_dict)
accuracy_df.to_csv('accuracy_gradientboosting.csv',index=False) 




		
		





