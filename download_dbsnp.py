#!/usr/bin/python3

import os

download_base_url = "ftp://ftp.ncbi.nih.gov/snp/latest_release/JSON/refsnp-chr"


# create downloading URLs for dbSNP
url_list1 = [download_base_url + str(i) for i in list(range(1,23)) + ['MT', 'X', 'Y']]

url_list = [base_url + ".json.bz2" for base_url in url_list1]

file_list1 = ['refsnp-chr' + str(i) for i in list(range(1,23)) + ['MT', 'X', 'Y']]

file_list = [base_file_name + ".json.bz2" for base_file_name in file_list1]

for url,file_name in zip(url_list,file_list):
    command = "curl " + url + " --retry 10 --retry-max-time 0 -C - > ./data/" + file_name
    print("wget -c " + url)
