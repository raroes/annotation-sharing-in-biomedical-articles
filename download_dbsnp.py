#!/usr/bin/python3

import os
from init_vars import *

#download_base_url = "ftp://ftp.ncbi.nih.gov/snp/latest_release/JSON/refsnp-chr"
download_base_url = "ftp://ftp.ncbi.nih.gov/snp/archive/b153/JSON/refsnp-chr"
download_directory = "./data/"


# create downloading URLs for dbSNP
url_list1 = [download_base_url + str(i) for i in list(range(1,23)) + ['MT', 'X', 'Y']]

url_list = [base_url + ".json.bz2" for base_url in url_list1]

file_list1 = ['refsnp-chr' + str(i) for i in list(range(1,23)) + ['MT', 'X', 'Y']]

file_list = [base_file_name + ".json.bz2" for base_file_name in file_list1]

for url,file_name in zip(url_list,file_list):
    command = "wget -c " + url + " -P " + download_directory
    print(command)
    os.system(command)
