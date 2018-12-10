from process_and_categorize import classiFier
import os
import time

start_time = time.time()
root_dir = os.getcwd()

model_name = 'randomforestx0.5x1.0x0.01x0.01'
model_file = os.path.join(root_dir,'random_forest_model',model_name)
classifierType = 'randomforest'
test_dir = os.path.join(root_dir,'Long_recording_test')

classifier0 = classiFier(test_dir , model_file, classifierType, verbose=True, num_threads=0)
classifier0.classify()
print 'time taken: ', str(time.time() - start_time) + ' seconds'
