#!/usr/bin/python3

# this script computes individual-record recall

import sys

input_citation_file = "pmid_citations.txt"
input_file = "pmid_annotations.txt"
output_file = "bc2gn_annotation_recall.txt"

f_in = open(input_file, "r")

# read existing annotations

print("Reading annotations...")
annotations_pmid = {}
pmids = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        annotations_pmid[pmid] = data[1]
        pmids[pmid] = 1
        counter_annotations += len(annotations_pmid[pmid].split("|"))

print("Annotations read: " + str(counter_annotations))


citation_counter_all = {}
citation_counter_annotations = {}
counter = 0

# read available citation data
print("Reading citation data...")
shared_annotations = {}
f_in = open(input_citation_file)

for line in f_in:
    data = line[:-1].split("\t")
    counter+=1
    if counter / 1000000 == int(counter / 1000000):
        print("Read " + str(counter) + " citations")
    if len(data) > 1:
        pmid1 = data[0]
        pmid2 = data[1]
        pmids[pmid1] = 1
        pmids[pmid2] = 1
        if pmid1 in citation_counter_all.keys():
            citation_counter_all[pmid1] += 1
        else:
            citation_counter_all[pmid1] = 1
        if pmid2 in citation_counter_all.keys():
            citation_counter_all[pmid2] += 1
        else:
            citation_counter_all[pmid2] = 1
        # check if first PMID is annotated
        if pmid1 in annotations_pmid.keys():
            # check if second PMID is annotated
            if pmid2 in annotations_pmid.keys():
                if pmid1 in citation_counter_annotations.keys():
                    citation_counter_annotations[pmid1] += 1
                else:
                    citation_counter_annotations[pmid1] = 1
                if pmid2 in citation_counter_annotations.keys():
                    citation_counter_annotations[pmid2] += 1
                else:
                    citation_counter_annotations[pmid2] = 1
                annotations1 = annotations_pmid[pmid1].split("|")
                annotations2 = annotations_pmid[pmid2].split("|")    
                # count annotations that the second PMID shared with the first 
                for annotation in annotations2:
                    if annotation in annotations1:
                        if pmid1 in shared_annotations.keys():
                            if annotation not in shared_annotations[pmid1]:
                                shared_annotations[pmid1].append(annotation)
                        else:
                            shared_annotations[pmid1] = [annotation]
                # same as before but reverse
                for annotation in annotations1:
                    if annotation in annotations2:
                        if pmid2 in shared_annotations.keys():
                            if annotation not in shared_annotations[pmid2]:
                                shared_annotations[pmid2].append(annotation)
                        else:
                            shared_annotations[pmid2] = [annotation]

# compute recall for each PMID based on the previous counts

print("Writing output file " + output_file + "...")

f_out = open(output_file, "w")
f_out.write("PMID\tShared annotations\tTotal\tRecall\tConnections with annotations\tTotal connections\n")
recall_all = {}
recall_annotated = {}
for pmid in annotations_pmid.keys():
    total = len(annotations_pmid[pmid].split("|"))
    if pmid in shared_annotations.keys():
        shared = len(shared_annotations[pmid])
    else:
        shared = 0
    if pmid in citation_counter_annotations.keys():
        count_annotations = citation_counter_annotations[pmid]
    else:
        count_annotations = 0
    if pmid in citation_counter_all.keys():
        count_all = citation_counter_all[pmid]
    else:
        count_all = 0
    if total > 0:
        recall = shared / total
        f_out.write(str(pmid) + "\t" + str(shared) + "\t" + str(total) + "\t" + str(recall) + "\t" + str(count_annotations) + "\t" + str(count_all) + "\n")

