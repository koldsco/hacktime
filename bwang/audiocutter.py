#!/usr/bin/python

import argparse
from subprocess import Popen, PIPE, check_output, CalledProcessError
import os,sys
import wave
import contextlib
import speech_recognition as sr
import os
import json
import collections
import time

def extract(filename):
    r = sr.Recognizer()
    with sr.WavFile(filename) as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file
        return r.recognize_google(audio)

def ffm(infile,timelen,timestart,outfile):
    try:
        print """ffmpeg -i %s -t "%s" -ss "%s" %s"""%(infile,timelen,timestart,outfile)
        check_output("""ffmpeg -i %s -t "%s" -ss "%s" %s"""%(infile,timelen,timestart,outfile),shell=True)
    except CalledProcessError as e:
        print "ffmpeg failed(%s): %s"%(e.returncode,e.output)
        sys.exit(1)


parser = argparse.ArgumentParser(description='Cut this audio!')
parser.add_argument('INFILE',help="The audio infile")
parser.add_argument('TIME',help="how long for pieces")
parser.add_argument('OUTDIR',help="where does it spit out files")
args = parser.parse_args()

with contextlib.closing(wave.open(args.INFILE,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print """file is %s s long"""%duration

for i in range(0,int(duration),int(args.TIME)):
    out = "%s/%s_%s.wav"%(args.OUTDIR,args.INFILE,str(i).zfill(3))
    ffm(args.INFILE,args.TIME,i,out)

result = {}

counter = 0
COUNTER_LIMIT = 5
for filename in os.listdir(os.getcwd()):
   # wav file and smaller than 10
   if 'wav' in filename.lower() and os.path.getsize(filename) < 10000000:
       try:
           text = extract(filename)
           os.remove(filename)
           print filename
           print text
           print '------------------'
           result[filename] = text
           if counter > COUNTER_LIMIT:
               break
           else:
               counter = counter + 1 
       except: 
           pass
           #print sys.exc_info()

print result

od = collections.OrderedDict(sorted(result.items()))
for k,v in od.iteritems():
    print k, v

file_result = open('result.json', 'w')
file_result.write(json.dumps(result))
file_result.close()
