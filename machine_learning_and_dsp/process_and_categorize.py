#! python

#This file contains functions to classify files recorded by the device

import cPickle
import shutil
import sys
import time
from zlib import crc32

import MySQLdb
import _mysql_exceptions
import pathos.multiprocessing as mp
from pathos.multiprocessing import Pool
from pyAudioAnalysis import audioTrainTest as aT
from pymediainfo import MediaInfo

from config import *
from noise_removal import noiseCleaner


#This function creates a new sql table for the classifier data automatically if it does not already exist
def tbl_create():
    tbl_create = os.path.join(os.getcwd(), 'tbl_create.sql')
    if os.system("mysql -u %s -p %s --password=%s < %s" % (user, database, passwd, tbl_create)):
        raise Exception("tbl_create.sql error!")

#The classifier object
#directory is the directory containing the wav files from the device if you wish to classify an entire directory at once
#model_file is the path of the model file which should also contain model_file.arff and model_fileMEANS; however, this paramater should be pointed to model_file
#classifierType is the ML algorithm that was used to train the model, see pyAudioAnalysis and scikit-learn docs for more info
#verbose prints a line to stdout for each file classified including its results
#num_threads is the number of processes to run in paralel, default is the number of logical cores on your p.c., this will NOT work correctly on flux and must be set manually in that case
class classiFier:
    def __init__(self, directory=os.getcwd(), model_file=os.path.join(os.getcwd(), 'model'),
                 classifierType='gradientboosting',
                 verbose=False, num_threads=mp.cpu_count()):
        self.directory = directory
        self.model_file = model_file
        self.classifierType = classifierType
        self.verbose = verbose
        self.num_threads = num_threads

        try:
            db = MySQLdb.connect(host=host, user=user, passwd=passwd,
                                 db=database)
        except _mysql_exceptions.OperationalError, e:
            if e[0] != 1049:
                raise
            else:
                with MySQLdb.connect(host=host, user=user, passwd=passwd,
                                     db='') as cur:
                    cur.execute("CREATE DATABASE %s;" % database)
        else:
            db.close()

    #This function classifies all files in the directory and puts the results into the sql table
    #it will also print the results to stdout if verbose was set to true
    def classify(self):
        directory = self.directory
        num_threads = self.num_threads

        wav_files = []
        for file in os.listdir(directory):
            if file.endswith('.wav') or file.endswith('.WAV'):
                file = os.path.join(directory, file)
                wav_files.append(file)
                if not num_threads:
                    self.classFile(file)
        
        if num_threads:
            try:
                pros = Pool(num_threads)
                pros.map(self.classFile, wav_files)
            except cPickle.PicklingError:
                for wfile in wav_files:
                    self.classFile(wfile)
        if os.path.exists(os.path.join(directory, "noise")):
            shutil.rmtree(os.path.join(directory, "noise"))
        if os.path.exists(os.path.join(directory, "activity")):
            shutil.rmtree(os.path.join(directory, "activity"))

    #This function classifies a single file and puts the results into the sql table
    #it will also print the results to stdout if verbose was set to true
    def classFile(self, file, username=None):
        model_file = self.model_file
        classifierType = self.classifierType
        verbose = self.verbose

        added = os.path.getmtime(file)
        added = time.gmtime(added)
        added = time.strftime('\'' + '-'.join(['%Y', '%m', '%d']) + ' ' + ':'.join(['%H', '%M', '%S']) + '\'',
                              added)

        cleaner = noiseCleaner(verbose=verbose)
        clean_wav = cleaner.noise_removal(file)
        Result, P, classNames = aT.fileClassification(clean_wav, model_file, classifierType)
        if verbose:
            print file
            print Result
            print classNames
            print P, '\n'

        result_dict = {}
        for i in xrange(0, len(classNames)):
            result_dict[classNames[i]] = P[i]

        result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

        with open(file, 'rb') as file_contents:
            sample_id = crc32(file_contents.read())

        device_id = -1  # tbi

        file_metadata = MediaInfo.parse(file)
        file_metadata = file_metadata.tracks[0]
        assert file_metadata.track_type == 'General'
        humidity = file_metadata.humi
        temp = file_metadata.temp
        latitude = file_metadata.lati
        longitude = file_metadata.long
        light = file_metadata.lite

        if humidity == None or humidity == ' nan':
            humidity = -1
        else:
            humidity = float(humidity)

        if temp == None or temp==' nan':
            temp = -1
        else:
            temp = float(temp)

        if latitude == None:
            latitude = 999.0
        else:
            latitude = float(latitude)

        if longitude == None:
            longitude = 999.0
        else:
            longitude = float(longitude)

        if light == None or light == 0:
            light = -1
        else:
            light = float(light)

        type1 = '\'' + result_dict[0][0] + '\''
        type2 = '\'' + result_dict[1][0] + '\''
        type3 = '\'' + result_dict[2][0] + '\''
        per1 = result_dict[0][1]
        per2 = result_dict[1][1]
        per3 = result_dict[2][1]

        values = [sample_id, device_id, added, latitude, longitude, humidity, temp, light, type1, per1, type2,
                  per2,
                  type3, per3]
        if username:
            values.append("'" + username + "'")
        values = [str(x) for x in values]

        with MySQLdb.connect(host=host, user=user, passwd=passwd,
                             db=database) as cur:  # config is in config.py: see above
            if username:
                query_text = "INSERT INTO sampleInfo (sampleid, deviceid, added, latitude, longitude, humidity, temp, light, type1, per1, type2, per2, type3, per3, user) values(" + ','.join(
                    values) + ");"
            else:
                query_text = "INSERT INTO sampleInfo (sampleid, deviceid, added, latitude, longitude, humidity, temp, light, type1, per1, type2, per2, type3, per3) values(" + ','.join(
                    values) + ");"
            try:
                cur.execute(query_text)
            except _mysql_exceptions.ProgrammingError, e:
                if e[0] != 1146:
                    raise
                else:
                    tbl_create()
                    cur.execute(query_text)
            except _mysql_exceptions.IntegrityError, e:
                if e[0] != 1062:
                    raise
                else:
                    sys.stderr.write("Warning: Duplicate key entry.\n")

        return {"values": values, "sample_id": sample_id}



    #This function exports the entire sql table and all the included data to a .sql file that can then be imported into another sql server
    #somewhere else
    #This was mainly implemented due to design choices that were abondened somewhere along the way, but it may be useful to you at some point
    def export(self):
        try:
            export_file = str(time.time())
            dump_command = "mysqldump -u %s -p %s --password=%s --skip-add-drop-table --no-create-info --skip-add-locks > export/%s.sql" % (
            user, database, passwd, export_file)
            if not os.path.exists('export'):
                os.mkdir('export')
            if os.system(dump_command):
                raise Exception("mysqldump export failed! Rerun for details: %s" % dump_command)
        except:
            raise
        else:
            with MySQLdb.connect(host=host, user=user, passwd=passwd,
                                 db=database) as cur:
                cur.execute("DROP DATABASE %s;" % database)
                cur.execute("CREATE DATABASE %s;" % database)

            tbl_create()
