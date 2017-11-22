from noise_removal import noiseCleaner
if __name__ == '__main__':
    rootdir = "E:\\bird_model_2\\Testing"
    new_cleaner = noiseCleaner(verbose=True, num_threads=4)
    new_cleaner.noise_removal_dir(rootdir)
    # for root, dirs, files in os.walk(rootdir):
    #     print dirs
