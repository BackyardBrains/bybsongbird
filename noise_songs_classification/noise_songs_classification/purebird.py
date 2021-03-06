# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 15:52:59 2018

@author: Xiaoran Peng
"""
import numpy as np
import librosa
#import matplotlib.pyplot as plt
import scipy.fftpack as sf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.externals import joblib
from pydub import AudioSegment
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
#can be change input part
file_name = 'D:/songs/The_birds_I_have/common_loon.wav'#original sound
AudioSegment.converter = "C:/Users/Xiaoran Peng/Downloads/ffmpeg-20181111-e24a754-win64-static/ffmpeg-20181111-e24a754-win64-static/bin/ffmpeg"
sound = AudioSegment.from_wav(file_name)
#sff,long=wavfile.read(file_name)
long=librosa.core.load(file_name, sr=44100)[0]
number_of_chunk=25
clf = joblib.load('D:\\knn27.pkl')#the model
threshold=0.2#0.2,1,0
length=1000#3000,5000
name='D:/songs/The_birds_I_have/common_loon00.wav'#saved file name

def testandcut(sound,loadsong):
    i=0
    total=sound[0]
    noisetotal=sound[0]
    while (i+1)*length<len(sound):
#          print(i)
          temp=sound[i*length:length*(i+1)]
          fortest=long[int(i*44100*length/1000):int(44100*(i+1)*length/1000)]
          if testsongs(fortest)==1:
              total=total+temp
          else:
              noisetotal=noisetotal+temp
          i=i+1
    total=total+sound[i*length:len(sound)-1]
    total.export(name, format="wav",tags={'artist': 'crow'})
    noisetotal.export(name[0:len(name)-4]+'noise.wav',format="wav",tags={'artist': 'crow'})

def testsongs(l):
    if len(l)!=44100:
        return 0
    l0=normal(l)
    ltotal=sum(l)#    if len(l)<37500:
#        print(str(i)+'less')
    
    lf=np.array(sf.fft(l0)[1:][0:22050])
    
    lfenergy10=find_mean_energy(np.abs(lf)*np.abs(lf),number_of_chunk,ltotal)
#    list(lfenergy10).append(ltotal)
    prob=clf.predict_proba([lfenergy10])
#    print(prob)
    if prob[0][0]>=threshold:
       return 1
    else:
       return 0
testandcut(sound,long)
          