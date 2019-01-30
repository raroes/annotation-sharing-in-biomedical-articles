#!/usr/bin/python3

input_file = "pmid_annotations.txt"
input_citation_file = "pmid_citations.txt"

output_file = "neighborhood_annotation_statistics.txt"

# read a list of annotations
f_in = open(input_file, "r")

print("Reading annotations...")
annotations_pmid = {}
pmids = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        # create a dictionary of annotations for each PMID
        annotations_pmid[pmid] = data[1]
        pmids[pmid] = 1
        for annotation in annotations_pmid[pmid].split("|"):
            counter_annotations += 1

print("Annotations read: " + str(counter_annotations))
print("PMIDs read: " + str(len(pmids.keys())))

counter=0
pmid_connections = {}

print("Reading citation data...")

# read the file with citation data, which is a list of PMID pairs
f_in = open(input_citation_file)

all_connection_count = {}
annotated_connection_count = {}
for line in f_in:
    data = line[:-1].split("\t")
    counter+=1
    if counter / 1000000 == int(counter / 1000000):
        print("Read " + str(counter) + " connections.")
    if len(data) > 1:
        # for each pair of PMIDs
        pmid1 = data[0]
        pmid2 = data[1]
        # check if the first PMID is annotated
        if pmid1 in pmids.keys():
            if pmid1 in all_connection_count.keys():
                all_connection_count[pmid1] += 1
            else:
                all_connection_count[pmid1] = 1
            # check if the second PMID is annotated
            if pmid2 in pmids.keys():
                if pmid1 in annotated_connection_count.keys():
                    annotated_connection_count[pmid1] += 1
                else:
                    annotated_connection_count[pmid1] = 1
        # do the same but now in reverse
        if pmid2 in pmids.keys():
            if pmid2 in all_connection_count.keys():
                all_connection_count[pmid2] += 1
            else:
                all_connection_count[pmid2] = 1
            if pmid1 in pmids.keys():
                if pmid2 in annotated_connection_count.keys():
                    annotated_connection_count[pmid2] += 1
                else:
                    annotated_connection_count[pmid2] = 1

annotated_count_list = {}
all_count_list = {}

annotated_count_list[0] = 0
all_count_list[0] = 0

# go back to each PMID and count statistics on number of annotated and not-annotated neighbors
for pmid in pmids:
    # statistics on annotated neighbors
    if pmid in annotated_connection_count.keys():
        count = annotated_connection_count[pmid]
        if count in annotated_count_list.keys():
            annotated_count_list[count] += 1
        else:
            annotated_count_list[count] = 1
    else:
        count = 0
        annotated_count_list[count] += 1
    # statistics on non-annotated neighbors
    if pmid in all_connection_count.keys():
        count = all_connection_count[pmid]
        if count in all_count_list.keys():
            all_count_list[count] += 1
        else:
            all_count_list[count] = 1
    else:
        count = 0
        all_count_list[count] += 1

total_pmids = len(pmids.keys()) 

# Write statistics output in a table
print("Writing output to " + output_file + "...")

f_out = open(output_file, "w")

f_out.write("Connection count" + "\t" + "With annotated connections" + "\t" + "Percentage of all records" + "\t" + "All connections" + "\t" + "Percentage of all records\n")

for i in range(0,max(all_count_list.keys())+1):
    if i in annotated_count_list.keys():
        annotated_count = annotated_count_list[i]
        percentage_annotated_count = annotated_count_list[i] / total_pmids
    else:
        annotated_count = 0
        percentage_annotated_count = 0
    if i in all_count_list.keys():
        percentage_all_count = all_count_list[i] / total_pmids
        all_count = all_count_list[i]
    else:
        percentage_all_count = 0
        all_count = 0
    f_out.write(str(i) + "\t" + str(annotated_count) + "\t" + str(percentage_annotated_count) + "\t" + str(all_count) + "\t" + str(percentage_all_count) + "\n")
