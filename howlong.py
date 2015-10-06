#!/usr/bin/python

import wave,contextlib,sys

print sys.argv[1]

with contextlib.closing(wave.open(sys.argv[1],'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print """file is %s s long"""%duration

