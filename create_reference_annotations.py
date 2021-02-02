#!/usr/bin/python3

import sys, os

input_file = "pmid_mesh.txt"
group_names = ["L1000", "NLM2007", "S200"]

pmids = {}

for group_name in group_names:
    f_in = open("./data/" + group_name + ".pmids", "r")
    for line in f_in:
        pmid = line[:-1]
        pmids[pmid] = group_name
    if os.path.isfile("pmid_mesh_" + group_name + ".txt"):
        os.remove("pmid_mesh_" + group_name + ".txt")    

f_in = open(input_file)

for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid in pmids.keys():
        group_name = pmids[pmid]
        f_out = open("pmid_mesh_" + group_name + ".txt", "a")
        mesh_terms = data[1].split("|")
        for mesh_term in mesh_terms:
            f_out.write(pmid + "\t" + mesh_term + "\n")
        f_out.close() 
