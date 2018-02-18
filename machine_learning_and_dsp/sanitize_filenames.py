#! python
# -*- coding: utf-8 -*-

import os
import sys


#This function will remove any unicode characters or special characters from the names of your wav-files
#This is useful because python does not handle this well and it will break most of the functions in pyAudioAnalysis
#Other functions will call this automatically (look for a no-santize flag)
def sanatize_filenames(directory=unicode(os.getcwd()), verbose=False):
    if verbose:
        print "Now sanitizing filenames in root directory: ", directory, '\n'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav') or file.endswith('WAV'):
                filename, fileextension = os.path.splitext(file)
                new_filename = ''.join(e for e in filename if e.isalnum()) + '.wav'
                file = os.path.join(root, file)
                new_filename = os.path.join(root, new_filename)
                while (os.path.exists(new_filename)):
                    new_filename += '1.wav'
                if file != new_filename:
                    os.rename(file, new_filename)
                if verbose:
                    print new_filename

    if verbose:
        print ''


#Allows you to run the function from shell recursively accross the current working directory
#meaning that all wav files in the directory and all subdirectories will be processed
if __name__ == '__main__':
    directory = unicode(os.getcwd())
    if len(sys.argv) > 1:
        directory = sys.argv[1]

    sanatize_filenames(directory)
