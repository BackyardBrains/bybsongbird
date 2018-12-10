import os 

directory = os.getcwd()

#directory = '/home/bybsongbird/machine_learning_and_dsp'

birds = []

path = os.path.join(directory, 'Training')

for root, dirs, files in os.walk(path):
    for bird in dirs:
	birds.append(bird)
    break
       
print birds
