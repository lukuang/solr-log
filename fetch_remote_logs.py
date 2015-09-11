"""
fetch remote log files for all path
"""
import os



paths = {1:"/home/yzhan/Desktop/running_solr/solr-4.10.0/DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2/logs/request*",
        2:"/home/yzhan/Desktop/running_solr/solr-4.10.0/DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new/logs/request*",
        3:"/home/yzhan/Desktop/running_solr/solr-4.10.0/DISCAT_NEWEST_AWSTAT_Final_labeling_New_Data_2_new_merge_fields/logs/request*"
}
dest_dir = "/home/lukuang/Desktop/process_solr_logs/logs"
for p in paths:
    sub_dest = os.path.join(dest_dir,str(p) )
    if not os.path.exists(sub_dest):
        os.mkdir(sub_dest)
    command_string = "scp yulin:%s %s" %(paths[p],sub_dest)
    print command_string
    os.system(command_string)