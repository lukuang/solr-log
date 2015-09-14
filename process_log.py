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
                print m.group(1),m.group(2),m.group(3)
            raw_input("press enter to continue")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_file","-l",default="/home/lukuang/Desktop/process_solr_logs/logs/all_logs")
    args = parser.parse_args()
    read_log(args.log_file)



if __name__=="__main__":
    main()