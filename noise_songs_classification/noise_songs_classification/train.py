# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:04:36 2018

@author: Xiaoran Peng
"""
import sys
#print ('Please enter the path of the traing file(noise), train file(bird songs) and chunk number:')
import os
rootdir = 'noise'
print(rootdir)
chunks=25
list1 = os.listdir(rootdir)
import numpy as np
import librosa
import matplotlib.pyplot as plt
import scipy.fftpack as sf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
def normal(song):
    waveData = song*1.0/(max(abs(song)))
    return waveData
audio=[]
target=[]
audiofft=[]
fftreal=[]
fftabs=[]
fftimag=[]
energy10=[] 
trainpath=[] 

def find_mean_energy(fftabs,num,total):
    l=int(len(fftabs)/num)
    energy=[]
    for i in range(num):
        temp=fftabs[i*l:(i+1)*l]
        tempsum=sum(temp)
        energy.append(tempsum)
    energy.append(total)
    return(np.array(energy))

for i in range(0,len(list1)):
    path = os.path.join(rootdir,list1[i])
    if os.path.isfile(path):
        if path[len(path)-3:len(path)]=='wav' or path[len(path)-3:len(path)]=='WAV':
           trainpath.append(path)
trainpath1=[]
rootdir = 'notnoise'
list2 = os.listdir(rootdir)
for i in range(0,len(list2)):
    path = os.path.join(rootdir,list2[i])
    if os.path.isfile(path):
        if path[len(path)-3:len(path)]=='wav' or path[len(path)-3:len(path)]=='WAV':
           trainpath1.append(path)
           


#
#
for i in range(len(trainpath)):
    inputfile=trainpath[i]
    l=librosa.core.load(inputfile, sr=44100)[0]
  
    l1=normal(l)
    l1total=sum(l)
    audio.append(l1)
    target.append(2)
    l1f=np.array(sf.fft(l1)[1:][0:22050])
    l1energy10=find_mean_energy(np.abs(l1f)*np.abs(l1f),chunks,l1total)
    audiofft.append(l1f)
    fftreal.append(l1f.real)
    fftabs.append(np.abs(l1f))
    energy10.append(l1energy10)#+l1total))
for i in range(len(trainpath1)):
    inputfile=trainpath1[i]
    l=librosa.core.load(inputfile, sr=44100)[0]
 
    l1=normal(l)
    l1total=sum(l)
    audio.append(l1)
    target.append(1)
    l1f=np.array(sf.fft(l1)[1:][0:22050])
    l1energy10=find_mean_energy(np.abs(l1f)*np.abs(l1f),chunks,l1total)
    audiofft.append(l1f)
    fftreal.append(l1f.real)
    fftabs.append(np.abs(l1f))
    #l1energy10.append(l1total)
    energy10.append(l1energy10)
from sklearn import svm
#clf = MultinomialNB()
clf=KNeighborsClassifier(n_neighbors=5)
clf.fit(energy10, target) 
joblib.dump(clf, 'D:\\knn1.pkl')
clf = joblib.load('D:\\knn1.pkl')#也可以使用文件对象
# clf = joblib.load('D:\\xxx\\data.pkl')
no=0
yes=0
energy10=np.array(energy10)
svmpredict=clf.predict(energy10)
svmprob=clf.predict_proba(energy10)
for i in range(len(svmpredict)):
    if svmpredict[i]==target[i]:
        yes=yes+1
    else:
#        plt.plot(fftreal[i])
#        plt.show()
        print(i)
        no=no+1
print('train on '+ str(len(list1)+len(list2))+' files ' +' accuracy is '+ str(yes/(yes+no)))

