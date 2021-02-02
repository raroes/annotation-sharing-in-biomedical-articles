#!/usr/bin/python3

# this script parses MESH annotations from the MEDLINE baseline

input = "new_pmid_annotations_mutations.txt"

from init_vars import *
import gzip
import os
import re

source_directories = source_directories_medline

output_file = "new_mutations_pmid.txt"


f_out = open(output_file, "w")

mesh_heading_area = 0
descriptor_names = []
found = 0
pmid = "0"
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
                # flag the MeshHeading areas
                line = line[:-1]
                if re.search("<MeshHeading>",line):
                    mesh_heading_area = 1
                    found = 0
                if re.search("</MeshHeading>",line):
                    mesh_heading_area = 0
                    descriptor_name = ""
                # if in MeshHeading area identify descriptor names
                if mesh_heading_area == 1:
                    if re.search("<DescriptorName[^\>]*>(.+)</DescriptorName>",line):
                        matched = re.search("<DescriptorName[^\>]*>(.+)</DescriptorName>",line)
                        descriptor_name = matched.group(1)
                        found = 1
                    # take only descriptor names that are major topic
                    if re.search("MajorTopicYN=\"Y\"",line):
                        if found == 1:
                            descriptor_names.append(descriptor_name)
                            found = 0
                # take the first PMID as the PMID of the record
                if pmid == "0":
                    if line.find("<PMID") > -1:
                        if re.search("<PMID.*>(.+)<\/PMID>", line):
                            matched = re.search("<PMID.*>(.+)<\/PMID>", line)
                            pmid = matched.group(1)
                # when the record ends write the output
                if line.find("</MedlineCitation") > -1:
                    if len(descriptor_names) > 0:
                        f_out.write(pmid + "\t" + "|".join(descriptor_names) + "\n")
                    pmid = "0"
                    descriptor_names = []
                    descriptor_name = ""
