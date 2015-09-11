"""
check merged log file by checking whether time
of each line is in ascending order
"""
import re
import os,sys
import time

dest_name = "/home/lukuang/Desktop/process_solr_logs/logs/all_logs"

previous = 0
with open(dest_name) as f:
    for line in f:
        #print line
        #m = re.search("\[(\d+/\w+/\d+:\d+:\d+:\d+)\s(\+|\-\d+)\]", line)
        m = re.search("\[(.+)\s(\+|\-)(\d{2})(\d{2})\]", line)
        if m is not None:
            t =  int(time.mktime(time.strptime(m.group(1),"%d/%b/%Y:%H:%M:%S") ))
            offset = int( m.group(3) )*3600 + int( m.group(4) )*60
            if m.group(2) == "+":
                offset *= -1
            t += offset
            if not (previous - t  <=120 or t>=previous):
                print "time error!"
                print "previous: %d, now %d" %(previous,t)
                print "line is:"
                print line
                sys.exit(-1)
            previous = t
        else:
            print "something wrong!"
            print line
            sys.exit(-1)
