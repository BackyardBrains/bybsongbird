from validate import validate

if __name__ == '__main__':
    directory = 'E:\\bird_model_2'
    classifierType = ['svm']
    mtStep = [0.4]
    mtWin = [0.4]
    stStep = [0.04]
    stWin = [0.04]
    num_threads = 18
    validate(directory=directory, classifierType=classifierType, mtStep=mtStep, mtWin=mtWin, stStep=stStep, stWin=stWin,
             num_threads=num_threads)
