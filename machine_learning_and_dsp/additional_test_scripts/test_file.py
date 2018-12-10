from pyAudioAnalysis import audioTrainTest as aT


model_file = 'gradientboostingx0.1x1.0x0.01x0.1'
classifierType = 'gradientboosting'
file = '24_44k.wav'
Result, P, classNames = aT.fileClassification(file, model_file, classifierType)

print Result
print P
print classNames
