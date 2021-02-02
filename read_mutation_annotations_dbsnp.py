#!/usr/bin/python3

# this script reads mutation annotations from the dbSNP database
input_file = "pmid_annotations_mutations.txt"
output_file = "pmid_annotations_dbsnp.txt"

print("Processing dbSNP annotations")

import gzip

# open the dbSNP file
f = open(input_file, 'r')

pmids_per_rs_id = {}
rs_ids_per_pmid = {}
rs_id_list = {}
total_annotations = 0
pmids = {}
# read all lines
print("Reading annotations...")
for line in f:
    line = line[:-1]
    # take information regarding rs ID and PMID
    data = line.split("\t")
    rs_id = data[1]
    pmid = data[0]
    # keep a list of all unique PMIDs
    pmids[pmid] = 1
    # keep a list of all unique rs IDs
    if rs_id not in rs_id_list.keys():
        rs_id_list[rs_id] = 1
    # for every rs ID, keep a list of all PMIDs in which it was annotated
    if rs_id not in pmids_per_rs_id:
        pmids_per_rs_id[rs_id] = [pmid]
        total_annotations += 1
    else:
        if pmid not in pmids_per_rs_id[rs_id]:
            pmids_per_rs_id[rs_id].append(pmid)
            total_annotations += 1
    # for every PMID, keep a list of all rs IDs that were annotated
    if pmid not in rs_ids_per_pmid:
        rs_ids_per_pmid[pmid] = [rs_id]
    else:
        if rs_id not in rs_ids_per_pmid[pmid]:
            rs_ids_per_pmid[pmid].append(rs_id)

print("Total (human) annotations: " + str(total_annotations))
print("Total number of mutations with annotations: " + str(len(rs_id_list.keys())))
print("Total articles annotated: " + str(len(pmids.keys())))

# count the number of PMIDs associated to each rs ID
pmids_per_rs_id_count = {}
for rs_id in pmids_per_rs_id.keys():
   number_of_pmids = len(pmids_per_rs_id[rs_id])
   if number_of_pmids not in pmids_per_rs_id_count.keys():
       pmids_per_rs_id_count[number_of_pmids]=0
   pmids_per_rs_id_count[number_of_pmids]+=1

# write for each PMID all the rs IDs that were found
print("Writing output file...")

f_out = open(output_file, "w")
for pmid in rs_ids_per_pmid.keys():
    f_out.write(pmid + "\t" + "|".join(rs_ids_per_pmid[pmid]) + "\n")

print("Finished writing output file.\n")
