from train_model import train_model
from clean_and_test import test_params
import os


directory = os.getcwd()
birds = []
for root, dirs, files in os.walk(os.path.join(directory, 'Training')):
	for bird in dirs:
    		birds.append(bird)	
	break

all_parameters =[('gradientboosting',0.1,1,0.01,0.1) ,('gradientboosting',0.1,0.5,0.01,0.1)]
for parameters in all_parameters:
	classifierType = parameters[0]
	mtStep = parameters[1]
	mtWin = parameters[2]
	stStep = parameters[3]
	stWin = parameters[4]
	train_rootdir = os.path.join(directory, 'Training')
	train_dirs = test_params(train_rootdir, birds)
	model = 'x'.join([classifierType, str(mtStep), str(mtWin), str(stStep), str(stWin)])
	model_path = os.path.join(os.getcwd(), model)
	train_model(list_of_dirs=train_dirs, mtWin=mtWin, mtStep=mtStep, stWin=stWin, stStep=stStep,
                classifierType=classifierType, modelName=model)
