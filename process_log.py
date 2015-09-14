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
            m = re.search("^(.+?)\s+-\s+-\s+\[(.+?)\] \"(.+?) HTTP/1.1\"",line)
            if m is not None:
                ip,complex_time, url = m.group(1),m.group(2),m.group(3)
                url = urllib.unquote(url)
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

                paras = urlparse.parse_qs(urlparse.urlsplit(url).query)
                #print paras
                if "q" in paras:
                    q_filed = paras["q"][0]
                    query_string = ""
                    mqs = re.search("^Id:\d+\+?$", q_filed)

                    #skip only doc id query
                    if mqs is not None:
                        continue

                    mqs = re.search("(Id:(\d+)\+?)?(\S+)",q_filed)
                    if mqs is not None:
                        query_string =  mqs.group(3) 
                        if("relevent" in paras):
                            print "a relevance judgement"
                            if paras["relevent"][0].lower() == "true":
                                print "relevant!"
                            else:
                                print "non-relevant"
                        if mqs.group(1) is not None:
                            if "mlt" in paras:
                                print "a click"
                                print "doc id", mqs.group(2)
                             
                            else:
                                print "strange query with docid"
                                print line
                                raw_input("press enter to continue")
                    raw_input("press enter to continue")

                #if "mlt=true" in q_filed:
                #
                #elif "relevent=" in q_filed:
                #
                #else:

                
                
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