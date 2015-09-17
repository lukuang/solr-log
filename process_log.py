"""
process query log
"""
import re
import os,sys
import time
import argparse
import urllib,urlparse

def store_record(record,logs):
    if len(logs['queries']) == 0:
        return
    else:
        for query in logs['queries']:
            if query not in record:
                record[query] = []
            record[query] += logs['queries'][query]

        return

def read_log(log_file, session_threshold):
    logs = {}
    record = {}
    catched = 0
    ignore = 0
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
                    if ip not in logs:
                        logs[ip] = {}
                        logs[ip]['prev_time'] = t 
                        logs[ip]['queries'] = {}
                    elif(t - logs[ip]['prev_time'])>= session_threshold:
                        print "empty ip"
                        store_record(record,logs[ip])
                        logs[ip] = {}
                        logs[ip]['prev_time'] = t 
                        logs[ip]['queries'] = {}

                    mqs = re.search("(Id:(\d+) ?)?(.+)",q_filed)
                    if mqs is not None:
                        query_string =  mqs.group(3)
                        #print "original query %s with length %d" %(query_string, len(query_string))


                        if("relevent" in paras):
                            print "a relevance judgement"
                            judgement = "true"
                            if paras["relevent"][0].lower() == "true":
                                print "relevant!"
                            else:
                                judgement = "false"
                                print "non-relevant"
                            if len(logs[ip]['queries'][query_string])==1:
                                logs[ip]['queries'][query_string][0]["relevance"] = judgement
                                catched += 1
                            else:
                                print "more than one document clicked, discard the judgement"
                                ignore +=1
                        if mqs.group(1) is not None:
                            if "mlt" in paras:
                                print "a click"
                                print "doc id", mqs.group(2)
                                if query_string not in logs[ip]['queries']:
                                    #print "insert query", query_string
                                    #print "length",len(query_string)
                                    logs[ip]['queries'][query_string] = []
                                else:
                                    logs[ip]['queries'][query_string][-1]["dur_time"] = t-logs[ip]['queries'][query_string][-1]["time"]
                                    if logs[ip]['queries'][query_string][-1]["dur_time"] <0:
                                        print "negative dur time!"
                                        print logs[ip]
                                single = {}
                                single["time"] = t
                                single["docid"] =  mqs.group(2)
                                single["dur_time"] = -1
                                single["ip"] = ip
                                single["relevance"] = "NA"

                                logs[ip]['queries'][query_string].append(single)

                            #else:
                            #    print "strnage sentence with doc id"
                            #    print line
                            
                    #raw_input("press enter to continue")

                #if "mlt=true" in q_filed:
                #
                #elif "relevent=" in q_filed:
                #
                #else:

                
                
            else:
                print "error line!"
                print line
            #raw_input("press enter to continue")
    for ip in logs:
        store_record(record,logs[ip])
    print record
    print "catched %d, ignore %d" %(catched,ignore)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_file","-l",default="/home/lukuang/Desktop/process_solr_logs/logs/all_logs")
    parser.add_argument("--session_threshold","-s",type=int, default=1800)

    args = parser.parse_args()
    read_log(args.log_file,args.session_threshold)



if __name__=="__main__":
    main()