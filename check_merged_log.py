"""
check merged log file by checking whether time
of each line is in ascending order
"""
import re
import os
import time

dest_name = "/home/lukuang/Desktop/process_solr_logs/logs/all_logs"

previous = ""
with open(dest_name) as f:
    for line in f:
        print line
        #m = re.search("\[(\d+/\w+/\d+:\d+:\d+:\d+)\s(\+|\-\d+)\]", line)
        m = re.search("\[(.+)\s(.+)\]", line)
        if m is not None:
            print m.group(1), m.group(2)
        #t =  int(time.mktime(time.strptime(time_part_1,"%d/%b/%Y:%H:%M:%S") ))
        else:
            print "something wrong!"
        raw_input("Press Enter to Continue")