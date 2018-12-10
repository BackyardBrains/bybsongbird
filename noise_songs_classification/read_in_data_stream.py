# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 16:09:01 2018

@author: Xiaoran Peng

cut large file to small pieces
"""

import time
start = time.clock()
import os
import wave
import numpy as np
class wave_Cut:
    def __init__(self, cut_time, path):
        self.cut_time = cut_time
        self.path = path
        self.files = os.listdir(path)
        
        for root,dire,name in os.walk(self.path):
            break
        self.names=name
        self.files = [path+'\\'+f for f in name if f.endswith('.wav')]
    def create_subdirectory(self,directory, subdir):
        if not os.path.exists(os.path.join(directory, subdir)):
            os.makedirs(os.path.join(directory, subdir))
    def CutFile(self):
        self.create_subdirectory(self.path, 'cutresults')
        for i in range(len(self.files)):
            FileName = self.files[i]
            tempname=self.names[i]
            print("CutFile File Name is ",FileName)
            f = wave.open(FileName, "rb")
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            CutFrameNum = framerate * self.cut_time
            str_data = f.readframes(nframes)
            f.close()
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            temp_data = wave_data.T
            StepNum = CutFrameNum
            StepTotalNum = 0;
            haha = 0
            while StepTotalNum < nframes:
                FileName = self.path+"\\cutresults\\" + tempname[0:len(tempname)-4] +"-"+ str(haha+1) + ".wav"
                temp_dataTemp = temp_data[StepNum * (haha):StepNum * (haha + 1)]
                if len(temp_dataTemp)<1:
                    break      
                haha = haha + 1;
                StepTotalNum = haha * StepNum;
                temp_dataTemp.shape = 1, -1
                temp_dataTemp = temp_dataTemp.astype(np.short)
                f = wave.open(FileName, "wb")#
                f.setnchannels(nchannels)
                f.setsampwidth(sampwidth)
                f.setframerate(framerate)
                f.writeframes(temp_dataTemp.tostring())
                f.close()
    return self.path+'\cutresults'

result=wave_Cut(cut_time=60,path='D:\songs\The_birds_I_have\wood_set')
final=result.CutFile()
elapsed = (time.clock() - start)
print("Time used:",elapsed)
#Cut large file to small pieces and read in stream
#cut_time is how long you would like to cut the original songs to (60 means 60 seconds)
#path is the directory of the original songs
#final means the final directory of the cutted songs
