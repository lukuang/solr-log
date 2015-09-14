"""
process query log
"""
import re
import os,sys
import time
import argparse


def read_log(log_file):
    with open(log_file) as f:
        for line in f:
            m = re.search("^(.+?)\s+-\s+-\s+\[(.+?)\] \"(.+?)\"",line)
            if m is not None:
                ip,complex_time, action = m.group(1),m.group(2),m.group(3)
                mt = re.match("(.+)\s(\+|\-)(\d{2})(\d{2})", complex_time)
                if mt is not None:
                    t =  int(time.mktime(time.strptime(mt.group(1),"%d/%b/%Y:%H:%M:%S") ))
                    offset = int( mt.group(3) )*3600 + int( mt.group(4) )*60
                    if mt.group(2) == "+":
                        offset *= -1
                    t += offset
                    print ip,t
                else:
                    print "error time format"
                    print line
                raw_input("press enter to continue")
            else:
                print "error line!"
                print line
            #raw_input("press enter to continue")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_file","-l",default="/home/lukuang/Desktop/process_solr_logs/logs/all_logs")
    args = parser.parse_args()
    read_log(args.log_file)



if __name__=="__main__":
    main()