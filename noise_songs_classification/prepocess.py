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

from scipy.io import wavfile

class noiseRemover:
    def __init__(self, chucks=25, threshold=0.4, length=1000,verbose=False):
        self.chucks = chucks
        self.threshold = threshold
        self.length = length
        self.verbose = verbose
    def create_subdirectory(self, dir, subdir):
        if not os.path.exists(os.path.join(dir, subdir)):
            os.makedirs(os.path.join(dir, subdir))
    def find_mean_energy(self,fftabs,num,total):
        l=int(len(fftabs)/num)
        energy=[]
        for i in range(num):
            temp=fftabs[i*l:(i+1)*l]
            tempsum=sum(temp)
            energy.append(tempsum)
        energy.append(total)
        return(np.array(energy))
    def normal(self,song):
        waveData = song*1.0/(max(abs(song)))
        return waveData
    def testsongs(self,l,model):
        if len(l)!=int(44100*self.length/1000):
            return 0
        l0=self.normal(l)
        ltotal=sum(l)   
        lf=np.array(sf.fft(l0)[1:][0:int(22050*self.length/1000)])
        
        lfenergy10=self.find_mean_energy(np.abs(lf)*np.abs(lf),self.chucks,ltotal)
        prob=model.predict_proba([lfenergy10])
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
        while (i+1)*self.length<len(sound):
              temp=sound[i*self.length:self.length*(i+1)]
              fortest=long[int(i*44100*self.length/1000):int(44100*(i+1)*self.length/1000)]
              if self.testsongs(fortest,clf)==1:
                  total=total+temp
              else:
                  noisetotal=noisetotal+temp
              i=i+1
        total=total+sound[i*self.length:len(sound)-1]
        dir, inputFile = os.path.split(inputFile)
        self.create_subdirectory(dir, 'clean')
        total.export(dir+'/clean/'+inputFile[0:len(inputFile)-4]+'_clean.wav', format="wav",tags={'artist': 'bird'})
        return dir+'/clean'+inputFile[0:len(inputFile)-4]
result=noiseRemover(verbose=True)
final=result.cutnoise('D:/songs/The_birds_I_have/wood.wav','D:\\knn27_0.18.1.pkl')
# chucks=25, threshold=0.4, length=1000 is related to the model, please do not change(I will provide best parameter for each model)
# Inputfile is the directory of the original file and inputModel is the directory of the model
# return the directory of the noise removed songs
# if you want to deal with many songs in a directory please use a for loop as below.
#rootdir = 'D:/songs/3_seconds_noise'
#list1 = os.listdir(rootdir)
#for i in range(0,len(list1)):
#    path = os.path.join(rootdir,list1[i])
#    if os.path.isfile(path):
#        if path[len(path)-3:len(path)]=='wav' or path[len(path)-3:len(path)]=='WAV':
#            result=noiseRemover(verbose=True)
#            final=result.cutnoise(path,'D:\\knn27_0.18.1.pkl')
#cleaned_dir, inputFile_name = os.path.split(final)
#cleaned_dir is the directory for all the noise_removed songs
           