from validate import validate

if __name__ == '__main__':
    directory = 'E:\\bird_model_2'
    classifierType = ['svm']
    mtStep = [1.0, 0.5, 0.1]
    mtWin = [1.0, 0.5, 0.1]
    stStep = [0.1, 0.05, 0.01]
    stWin = [0.1, 0.05, 0.01]
    num_threads = 18
    validate(directory=directory, classifierType=classifierType, mtStep=mtStep, mtWin=mtWin, stStep=stStep, stWin=stWin,
             num_threads=num_threads, debug=False, skip_clean=True)
