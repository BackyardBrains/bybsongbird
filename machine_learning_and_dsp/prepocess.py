# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 09:16:57 2018

@author: Xiaoran Peng
"""
## In process_and_categorize.py
## After call cleaner = noiseCleaner(verbose=verbose) clean_wav = cleaner.noise_removal(file)
## call remover=noiseRemover(verbose=verbose) removed_wav=cleaner.cutnoise(file,modeldir)
## After this function replace all the cleaner below with remover
import numpy as np
import librosa
#import matplotlib.pyplot as plt
import scipy.fftpack as sf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.externals import joblib
from pydub import AudioSegment
import os
import shutil
import sys

def find_mean_energy(fftabs,num,total):
    l=int(len(fftabs)/num)
    energy=[]
    for i in range(num):
        temp=fftabs[i*l:(i+1)*l]
        tempsum=sum(temp)
        energy.append(tempsum)
    energy.append(total)
    return(np.array(energy))
def normal(song):
    waveData = song*1.0/(max(abs(song)))
    return waveData
import wave
from scipy.io import wavfile
def create_subdirectory(dir, subdir):
    if not os.path.exists(os.path.join(dir, subdir)):
        os.makedirs(os.path.join(dir, subdir))
class noiseRemover:
    def __init__(self, chucks=25, threshold=0.2, length=1000,verbose=False):
        self.chucks = chucks
        self.threshold = threshold
        self.length = length
        self.verbose = verbose
    def testsongs(self,l,model):
        ltotal=sum(l)#    if len(l)<37500:
    #        print(str(i)+'less')
        
        lf=np.array(sf.fft(l0)[1:][0:22050])
        
        lfenergy10=find_mean_energy(np.abs(lf)*np.abs(lf),self.chucks,ltotal)
    #    list(lfenergy10).append(ltotal)
        prob=model.predict_proba([lfenergy10])
    #    print(prob)
        if prob[0][0]>=self.threshold:
           return 1
        else:
           return 0
    def cutnoise(self,inputFile,inputModel):
        verbose = self.verbose
        chucks=self.chucks
        threshold=self.threshold
        length=self.length
        clf = joblib.load(inputModel)
        if verbose:
            print(inputFile)

        if not os.path.isfile(inputFile):
            raise Exception(inputFile + " not found!")
        if not os.path.isfile(inputModel):
            raise Exception(inputModel + " not found!")
        #This is the path for ffmepg.exe if there is error with ffmepg
        #AudioSegment.converter = "C:/Users/Xiaoran Peng/Downloads/ffmpeg-20181111-e24a754-win64-static/ffmpeg-20181111-e24a754-win64-static/bin/ffmpeg"
        sound = AudioSegment.from_wav(inputFile)
        #sff,long=wavfile.read(file_name)
        long=librosa.core.load(inputFile, sr=44100)[0]
        i=0
        total=sound[0]
        noisetotal=sound[0]
        while (i+1)*length<len(sound):
    #          print(i)
              temp=sound[i*length:length*(i+1)]
              fortest=long[int(i*44100*length/1000):int(44100*(i+1)*length/1000)]
              if self.testsongs(fortest,clf)==1:
                  total=total+temp
              else:
                  noisetotal=noisetotal+temp
              i=i+1
        total=total+sound[i*length:len(sound)-1]
        dir, inputFile = os.path.split(inputFile)

        
        create_subdirectory(dir, 'noisenew')
        create_subdirectory(dir, 'activity')
        root, current_sub_dir = os.path.split(dir)
        clean_dir = '_'.join([current_sub_dir, 'clean'])
        create_subdirectory(dir, clean_dir)
        finaldir=os.path.join(dir, clean_dir)
        total.export(str(finaldir)+'purebird.wav', format="wav",tags={'artist': 'bird'})
        return finaldir
       # noisetotal.export(somedir[0:len(name)-4]+'noise.wav',format="wav",tags={'artist': 'crow'})