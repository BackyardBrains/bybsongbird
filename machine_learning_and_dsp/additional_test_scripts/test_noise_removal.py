import cPickle
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
import pydub

def create_subdirectory(dir, subdir):
    if not os.path.exists(os.path.join(dir, subdir)):
        os.makedirs(os.path.join(dir, subdir))


# https://stackoverflow.com/questions/2890703/how-to-join-two-wav-files-using-python
def recombine_wavfiles(infiles, outfile):
    sound = [AudioSegment.from_wav(infile) for infile in infiles]
    sound = sum(sound)

    sound.export(outfile, format="wav")
    for file in infiles:
        os.remove(file)


def segment_audio(inputFile,smoothingWindow,weight):
    print 'entered segment_audio function'
    [Fs, x] = audioBasicIO.readAudioFile(inputFile)
    dir, inputFile = os.path.split(inputFile)

    create_subdirectory(dir, 'noise')
    create_subdirectory(dir, 'activity')

    create_subdirectory(dir,'clean')

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

def remove_noise(inputFile,sensitivity):
    dir, inputFile = os.path.split(inputFile)
    activity_out = os.path.join(dir, "activity", inputFile)
    noise_out = os.path.join(dir, "noise", inputFile)
    clean_out = os.path.join(dir, "clean", inputFile)
    print 'clean_dir:' , clean_out
    tfs = sox.Transformer()
    noise_profile_path = '.'.join([noise_out, 'prof'])
    tfs.noiseprof(noise_out, noise_profile_path)
    tfs.build(noise_out, '-n')
    tfs.clear_effects()
    tfs.noisered(noise_profile_path, amount=sensitivity)

    print 'activity_folder:', activity_out
    print 'clean_folder:', clean_out

    tfs.build(activity_out, clean_out)

if __name__ == '__main__':
    smoothingWindow = 0.4
    weight=0.4
    sensitivity=0.3
    current_dir = os.getcwd()
    input_dir = os.path.join(current_dir,'Noise_removal_test')
    name_of_file = '1684444k.wav'
    input_file = os.path.join(input_dir,name_of_file)
    print 'entering segment_audio function'
    segment_audio(input_file,smoothingWindow,weight)
    remove_noise(input_file,sensitivity)
