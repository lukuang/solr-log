"""
merge all log files
"""

import os

paths = ["/home/lukuang/Desktop/process_solr_logs/logs/1",
        "/home/lukuang/Desktop/process_solr_logs/logs/2",
       "/home/lukuang/Desktop/process_solr_logs/logs/3"]

dest_name = "/home/lukuang/Desktop/process_solr_logs/logs/all_logs"

all_files = {}

for p in paths:
    for a_file in list(os.walk(p))[0][2]:
        if a_file not in all_files:
            all_files[a_file] = []
        all_files[a_file].append(os.path.join(p,a_file))

out_f = open(dest_name,"w")
for a_file in sorted(all_files.keys() ):
    #print a_file
    for path in all_files[a_file]:
        with open(path) as f:
            file_text = f.read()
            out_f.write(file_text)
            #raw_input("Press Enter to Continue!")