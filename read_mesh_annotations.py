#!/usr/bin/python3

# this script maps MeSH terms to their IDs and counts number of annotations

import re

annotation_file = "pmid_mesh.txt"
output_annotation_file = "pmid_annotations.txt"

input_file = "./data/d2019.bin"

# read the IDs associates to each MeSH term
print("Reading MeSH mappings...")

f_in = open(input_file, "r")

ui_mesh_header = {}
for line in f_in:
    line = line[:-1]
    # read MeSH term
    if re.search("MH = (.*)", line):
        matched = re.search("MH = (.*)", line)
        mesh_header = matched.group(1)
    # read MeSH ID
    if re.search("UI = (.*)", line):
        matched = re.search("UI = (.*)", line)
        ui = matched.group(1)
        ui_mesh_header[mesh_header] = ui

# read file with MeSH annotations and map the MeSH terms to their IDs
f_in = open(annotation_file, "r")
f_out = open(output_annotation_file, "w")

print("Reading annotation file " + annotation_file + "...")

total_annotations = 0
ui_dict = {}
ui_pmid = {}
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    mesh_headers = data[1].split("|")
    for mesh_header in mesh_headers:
        # check if MeSH term can be mapped to ID
        if mesh_header in ui_mesh_header.keys():
            ui = ui_mesh_header[mesh_header]
            total_annotations += 1
            ui_dict[ui] = 1
            # keep mapping in a dictionary
            if pmid not in ui_pmid.keys():
                ui_pmid[pmid] = [ui]
            else:
                ui_pmid[pmid].append(ui)

# map all MeSH term annotations to their IDs
print("Writing output file " + output_annotation_file + "...")
for pmid in ui_pmid.keys():
    uis = "|".join(ui_pmid[pmid])
    f_out.write(pmid + "\t" + uis + "\n")

print("Total annotations: " + str(total_annotations))
print("Total number of MeSH terms with annotations: " + str(len(ui_dict.keys())))
print("Total articles annotated: " + str(len(ui_pmid.keys())))

