"""
process query log
"""
import re
import os,sys
import time
import argparse
import urllib,urlparse

def read_log(log_file, session_threshold):
    logs = {}
    with open(log_file) as f:
        for line in f:
            if "/solr/collection1/browse" not in line:
                #print "skip line",line
                continue
            m = re.search("^(.+?)\s+-\s+-\s+\[(.+?)\] \"(.+?)\"",line)
            if m is not None:
                ip,complex_time, url = m.group(1),m.group(2),m.group(3)

                #get time of each query
                t= 0
                mt = re.match("^(.+)\s(\+|\-)(\d{2})(\d{2})$", complex_time)
                if mt is not None:
                    t =  int(time.mktime(time.strptime(mt.group(1),"%d/%b/%Y:%H:%M:%S") ))
                    offset = int( mt.group(3) )*3600 + int( mt.group(4) )*60
                    if mt.group(2) == "+":
                        offset *= -1
                    t += offset
                    #print line
                    #print ip,t, q_filed, query_string
                else:
                    print "error time format"
                    print line

                #get query and possible docid, relevance judgement
                mq = re.search("browse/?\?\&?q\=([^\& ]+)",url)
                #paras = urlparse.urlsplit(url)
                #skip query without a valid query string
                if mq is None or mq.group(1) is None:
                    #print "skip no query actions"
                    #print line
                    #raw_input("press enter to continue")
                    continue
                q_filed = mq.group(1)
                query_string = ""
                mqs = re.search("^Id:\d+\+?$", q_filed)

                #skip only doc id query
                if mqs is not None:
                    # print "skip only doc id query"
                    # print q_filed
                    # print line
                    continue
                mqs = re.search("(Id:(\d+)\+?)?(\S+)",q_filed)
                if mqs is not None:
                    query_string = urllib.unquote( mqs.group(3) )
                    if mqs.group(1) is not None:
                        if "mlt=true" in line:
                            print "a click"
                            print "doc id", mqs.group(2)
                        elif("relevent=" in line):
                            print "a relevance judgement"
                        else:
                            print "strange query with docid"
                            print line
                            raw_input("press enter to continue")

                #if "mlt=true" in q_filed:
                #
                #elif "relevent=" in q_filed:
                #
                #else:

                
                raw_input("press enter to continue")
            else:
                print "error line!"
                print line
            #raw_input("press enter to continue")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_file","-l",default="/home/lukuang/Desktop/process_solr_logs/logs/all_logs")
    parser.add_argument("--session_threshold","-s",type=int, default=1800)

    args = parser.parse_args()
    read_log(args.log_file,args.session_threshold)



if __name__=="__main__":
    main()