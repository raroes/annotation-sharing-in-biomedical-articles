#!/usr/bin/python3

# this script parses MESH annotations from the MEDLINE baseline

from init_vars import *
import gzip
import os
import re

source_directories = source_directories_medline

output_file = "pmid_list.txt"


f_out = open(output_file, "w")

print("Reading MEDLINE files...")

pmid = ""
for source_directory in source_directories:
    print(source_directory)
    files = os.listdir(source_directory)
    # go through every file in MEDLINE
    for file in files:
        input_file = os.path.join(source_directory, file)
        if re.search("\.gz", input_file):
            print(input_file)
            f = gzip.open(input_file, "rt")
            for line in f:
                line = line[:-1]
                # take the first PMID as the PMID of the record
                if pmid == "":
                    if line.find("<PMID") > -1:
                        if re.search("<PMID.*>(.+)<\/PMID>", line):
                            matched = re.search("<PMID.*>(.+)<\/PMID>", line)
                            pmid = matched.group(1)
                # when the record ends write the output
                if pmid != "":
                    f_out.write(pmid + "\n")
                    pmid = ""
