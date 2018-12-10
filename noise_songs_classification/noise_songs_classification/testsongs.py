# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:33:41 2018

@author: Xiaoran Peng
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
import scipy.fftpack as sf
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import wave
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.externals import joblib
def normal(song):
    waveData = song*1.0/(max(abs(song)))
    return waveData
#import sys
#print ('Please enter the piece_number, piece_length, traing_model ,test_file, number_of_chunks, start_of_fft, end_of_fft:')
import os
#rootdir = sys.argv[-4]
#inputfile= rootdir
#clf =joblib.load(sys.argv[-5])
#number_of_chunk=int(sys.argv[-3])
#start_of_fft=int(sys.argv[-2])
#end_of_fft=int(sys.argv[-1])
#piece= int(sys.argv[-7])
#piece_length= int(sys.argv[-6])
#inputfile='crow.wav'
#clf = joblib.load('D:\\knn.pkl')
number_of_chunk=25
#start_of_fft=300
#end_of_fft=12050
#piece=20
#piece_length=37500
#l=librosa.core.load(inputfile, sr=44100)[0]
#temp=[]

def find_mean_energy(fftabs,num,total):
    l=int(len(fftabs)/num)
    energy=[]
    for i in range(num):
        temp=fftabs[i*l:(i+1)*l]
        tempsum=sum(temp)
        energy.append(tempsum)
    energy.append(total)
    return(np.array(energy))
testpath=[]
rootdir = 'notnoise'
list2 = os.listdir(rootdir)
for i in range(0,len(list2)):
    path = os.path.join(rootdir,list2[i])
    if os.path.isfile(path):
        if path[len(path)-3:len(path)]=='wav' or path[len(path)-3:len(path)]=='WAV':
           testpath.append(path)
clf = joblib.load('D:\\knn1.pkl') 
temp=[]       
for i in range(len(testpath)):
    inputfile=testpath[i]
    l=librosa.core.load(inputfile, sr=44100)[0]
    if len(l)!=44100:
        continue
    l0=normal(l)
    ltotal=sum(l)#    if len(l)<37500:
#        print(str(i)+'less')
    
    lf=np.array(sf.fft(l0)[1:][0:22050])
    
    lfenergy10=find_mean_energy(np.abs(lf)*np.abs(lf),number_of_chunk,ltotal)
#    list(lfenergy10).append(ltotal)
    prediction=clf.predict([lfenergy10])
    prob=clf.predict_proba([lfenergy10])
    temp.append([lfenergy10])
    print(inputfile,i,prediction,prob)
 

