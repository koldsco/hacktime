#!/usr/bin/python

import argparse
from subprocess import Popen, PIPE, check_output, CalledProcessError
import os,sys
import wave
import contextlib


parser = argparse.ArgumentParser(description='Cut this audio!')
parser.add_argument('INFILE',help="The audio infile")
parser.add_argument('TIME',help="how long for pieces")
parser.add_argument('OUTDIR',help="where does it spit out files")
args = parser.parse_args()




def ffm(infile,timelen,timestart,outfile):
        try:
        	print """ffmpeg -i %s -t "%s" -ss "%s" %s"""%(infile,timelen,timestart,outfile)
        	check_output("""ffmpeg -i %s -t "%s" -ss "%s" %s"""%(infile,timelen,timestart,outfile),shell=True)
#root@ip-172-31-13-126:/home/ubuntu# ffmpeg -i about_time.wav -t 00:00:02 -ss 00:00:00 fun.wav
        except CalledProcessError as e:
                print "ffmpeg failed(%s): %s"%(e.returncode,e.output)
                sys.exit(1)



#how long are you?
with contextlib.closing(wave.open(args.INFILE,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print """file is %s s long"""%duration

for i in range(0,int(duration),int(args.TIME)):
	out = "%s/%s.wav"%(args.OUTDIR,str(i).zfill(3))
	ffm(args.INFILE,args.TIME,i,out)



