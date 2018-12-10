# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 08:45:54 2018

@author: Xiaoran Peng
"""

from pydub import AudioSegment
file_name = "blue_jay.wav"
sound = AudioSegment.from_wav(file_name)

def cut(sound,j):
    i=0
    while (i+1)*1000<len(sound):
          print(i)
          temp=sound[i*1000:1000*(i+1)]
          save_name = j+str(i)+'.wav'

          temp.export(save_name, format="wav",tags={'artist': 'crow'})
          i=i+1
#for j in range(44,60):
#    if j==1 or j==10:
#        continue
#    inputfile=str(j)+"_sub_field_0.wav"
#    sound = AudioSegment.from_wav(inputfile)
cut(sound,'blue_jay')