# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 13:08:25 2018

@author: Xiaoran Peng
"""


import os
import shutil
import sys

import pathos.multiprocessing as mp
import pyAudioAnalysis.audioBasicIO as audioBasicIO
import pyAudioAnalysis.audioSegmentation as aS
import scipy.io.wavfile as wavfile
import sox
from pathos.multiprocessing import Pool
from pydub import AudioSegment


#Checks if a subdirectory exists in a directory and if not creates it
def create_subdirectory(dir, subdir):
    if not os.path.exists(os.path.join(dir, subdir)):
        os.makedirs(os.path.join(dir, subdir))


#This function combines a list of segmented wav files into a single wav file
#This is used to concatonate individual segments of "activity" or noise
#together into their respective wav files
# https://stackoverflow.com/questions/2890703/how-to-join-two-wav-files-using-python
def recombine_wavfiles(infiles, outfile):
    sound = [AudioSegment.from_wav(infile) for infile in infiles]
    sound = sum(sound)

    sound.export(outfile, format="wav")

    for file in infiles:
        os.remove(file)


#noise-reducer object for more info on smoothingWindow and Weight see here: https://github.com/tyiannak/pyAudioAnalysis/wiki/5.-Segmentation
#sensitivity is the parameter given to sox for noisered, see SoX documentation for more info on that
#setting debug to false will automatically delete the "activity" and "noise" files once the whole process is completed in order to save space
#Verbose will print a line to stdout for each file processed
#num_threads is the number of threads to run in paralel, default is the number of logical cores on your machine, this count will NOT be accurate for flux
class noiseCleaner:
    def __init__(self, smoothingWindow=0.4, weight=0.4, sensitivity=0.4, debug=True,
                 verbose=False, num_threads=mp.cpu_count()):
        self.smoothingWindow = smoothingWindow
        self.weight = weight
        self.sensitivity = sensitivity
        self.debug = debug
        self.verbose = verbose
        self.num_threads = num_threads

    #This function performs noise removal for a single file
    #in some cases the process will fail, either because the file is too short or because activity is constant and therfore a noise profile cannot be generated
    #in this case the function will simply make a copy of the original file into the "clean" folder to feed to the classifier
    def noise_removal(self, inputFile):
        smoothingWindow = self.smoothingWindow
        weight = self.weight
        sensitivity = self.sensitivity
        debug = self.debug
        verbose = self.verbose

        if verbose:
            print inputFile

        if not os.path.isfile(inputFile):
            raise Exception(inputFile + " not found!")

        [Fs, x] = audioBasicIO.readAudioFile(inputFile)  # read audio signal

        dir, inputFile = os.path.split(inputFile)

        try:
            create_subdirectory(dir, 'noise')
            create_subdirectory(dir, 'activity')

            root, current_sub_dir = os.path.split(dir)
            clean_dir = '_'.join([current_sub_dir, 'clean'])
            create_subdirectory(dir, clean_dir)
        except OSError, e:
            if e.errno != 17:
                raise
                # time.sleep might help here
            pass

        try:

            segmentLimits = aS.silenceRemoval(x, Fs, smoothingWindow / 10.0, smoothingWindow / 10.0, smoothingWindow,
                                              weight, False)  # get onsets
            prev_end = 0
            activity_files = []
            noise_files = []
            for i, s in enumerate(segmentLimits):
                strOut = os.path.join(dir, "noise", "{0:s}_{1:.3f}-{2:.3f}.wav".format(inputFile[0:-4], prev_end, s[0]))
                wavfile.write(strOut, Fs, x[int(Fs * prev_end):int(Fs * s[0])])
                noise_files.append(strOut)

                strOut = os.path.join(dir, "activity", "{0:s}_{1:.3f}-{2:.3f}.wav".format(inputFile[0:-4], s[0], s[1]))
                wavfile.write(strOut, Fs, x[int(Fs * s[0]):int(Fs * s[1])])
                activity_files.append(strOut)

                prev_end = s[1]

            strOut = os.path.join(dir, "noise",
                                  "{0:s}_{1:.3f}-{2:.3f}.wav".format(inputFile[0:-4], prev_end, len(x) / Fs))
            wavfile.write(strOut, Fs, x[int(Fs * prev_end):len(x) / Fs])
            noise_files.append(strOut)

            activity_out = os.path.join(dir, "activity", inputFile)
            noise_out = os.path.join(dir, "noise", inputFile)

            recombine_wavfiles(noise_files, noise_out)
            recombine_wavfiles(activity_files, activity_out)


            tfs = sox.Transformer()
            noise_profile_path = '.'.join([noise_out, 'prof'])
            tfs.noiseprof(noise_out, noise_profile_path)
            tfs.build(noise_out, '-n')
            tfs.clear_effects()
            tfs.noisered(noise_profile_path, amount=sensitivity)
            clean_out = os.path.join(dir, clean_dir, inputFile)
            tfs.build(activity_out, clean_out)

        except:
            original_file = os.path.join(dir, inputFile)
            sys.stderr.write("Sox error in noise reduction of file: %s.\n" % original_file)
            clean_out = os.path.join(dir, clean_dir, inputFile)
            shutil.copyfile(original_file, clean_out)
            with open(os.path.join(dir, clean_dir, 'NR_fail_record.log'), 'a') as fail_record:
                fail_record.write('%s\n' % original_file)

        if not debug:
            shutil.rmtree(os.path.join(dir, "noise"))
            shutil.rmtree(os.path.join(dir, "activity"))

        return clean_out
    
    #Performs noise_removal for an entire directory recursively, meaning that all wav files in all subdirectories will be processed
#    def noise_removal_dir(self, rootdir):
#
#        num_threads = self.num_threads
#
#        if not os.path.exists(rootdir):
#            raise Exception(rootdir + " not found!")
#
#        for root, dirs, files in os.walk(rootdir):
#            parent, folder_name = os.path.split(root)
#            if folder_name == 'activity' or folder_name == 'noise' or '_clean' in folder_name:
#                shutil.rmtree(root)
#        num_samples_processed = 0
#        wav_files = []
#        for root, dirs, files in os.walk(rootdir):
#            for file in files:
#                if file.endswith('.wav') or file.endswith('.WAV'):
#                    wav_files.append(os.path.join(root, file))
#                    num_samples_processed += 1
#                    if not num_threads:
#                        self.noise_removal(os.path.join(root,file))
#
#        print "Now beginning preprocessing for: ", num_samples_processed, " samples."
#
#        try:
#            if num_threads:
#                pros = Pool(num_threads)
#                pros.map(self.noise_removal, wav_files)
#        except cPickle.PicklingError:
#            for wfile in wav_files:
#                self.noise_removal(wfile)
#
#        print "Preprocessing complete!\n"