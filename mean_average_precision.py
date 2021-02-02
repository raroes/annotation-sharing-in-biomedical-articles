#!/usr/bin/python3

# compute recall, precision, F-measure and MAP

import sys
import re

if len(sys.argv) > 1:
    input_citation_file = sys.argv[1]
    input_file = sys.argv[2]
else:
    input_citation_file = "pmid_citations.txt"
    input_file = "pmid_annotations_gene2pubmed.txt"

input_file_trimmed = re.sub(r'^[\.]','',re.sub(r'[^a-zA-Z0-9i\_\.]', '', input_file))
input_citation_file_trimmed =  re.sub(r'^[\.]','',re.sub(r'[^a-zA-Z0-9\_\.]', '', input_citation_file))

output_file_f_measure = input_file_trimmed + "_" + input_citation_file_trimmed + "_" + "annotation_average_f_measure_based_on_connections1.txt"
output_file_map = input_file_trimmed + "_" + input_citation_file_trimmed + "_" + "annotation_map_based_on_connections1.txt"
output_figure_data = input_file_trimmed + "_" + input_citation_file_trimmed + "_" + "figure_data.txt"

f_in = open(input_file, "r")

# read annotation data
print("Reading annotations...")
annotations_pmid = {}
annotation_stats = {}
pmids = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        annotations_pmid[pmid] = data[1]
        pmids[pmid] = 1
        annotations = annotations_pmid[pmid].split("|")
        counter_annotations += len(annotations)
        for annotation in annotations:
            if annotation in annotation_stats.keys():
                annotation_stats[annotation] += 1
            else:
                annotation_stats[annotation] = 1

print("Annotations read: " + str(counter_annotations))

citation_counter_annotated = {}
citation_counter_all = {}
counter = 0

# read network connections
print("Reading citation data...")
neighborhood_annotations = {}
neighborhood_annotation_dict = {}
f_in = open(input_citation_file)
counter_neighbors = 0
counter_pairs = 0

for line in f_in:
    #for i in range(0,25):
    #    line = f_in.readline()
    counter+=1
    if counter / 100000000 == int(counter / 100000000):
        print("Read " + str(counter) + " citations")
    data = line[:-1].split("\t")
    if len(data) > 1:
        pmid1 = data[0]
        pmid2 = data[1]
        pmids[pmid1] = 1
        pmids[pmid2] = 1
        # compute overall connection counts
        if pmid1 in citation_counter_all.keys():
            citation_counter_all[pmid1] += 1
        else:
            citation_counter_all[pmid1] = 1
        if pmid2 in citation_counter_all.keys():
            citation_counter_all[pmid2] += 1
        else:
            citation_counter_all[pmid2] = 1
        # if PMID has been annotated then...
        if pmid1 in annotations_pmid.keys():
            # ... check if the other PMID has been annotated as well
            if pmid2 in annotations_pmid.keys():
                counter_pairs += 1
                # compute annotated connection counts
                if pmid1 in citation_counter_annotated.keys():
                    citation_counter_annotated[pmid1] += 1
                else:
                    citation_counter_annotated[pmid1] = 1
                if pmid2 in citation_counter_annotated.keys():
                    citation_counter_annotated[pmid2] += 1
                else:
                    citation_counter_annotated[pmid2] = 1
                # compare annotations between the first PMID and the second PMID
                annotations1 = annotations_pmid[pmid1].split("|")
                annotations2 = annotations_pmid[pmid2].split("|")    
                for annotation in annotations2:
                    # populate a list with all the annotations in the neighborhood of the first PMID
                    if pmid1 in neighborhood_annotations.keys():
                        neighborhood_annotation_dict = neighborhood_annotations[pmid1]
                    else:
                        neighborhood_annotation_dict = {}
                        counter_neighbors += 1
                    if annotation in neighborhood_annotation_dict.keys():
                        neighborhood_annotation_dict[annotation] += 1
                    else:
                        neighborhood_annotation_dict[annotation] = 1
                    neighborhood_annotations[pmid1] = neighborhood_annotation_dict
                # repeat the same process with the second PMID
                for annotation in annotations1:
                    if pmid2 in neighborhood_annotations.keys():
                        neighborhood_annotation_dict = neighborhood_annotations[pmid2]
                    else:
                        neighborhood_annotation_dict = {}
                        counter_neighbors += 1
                    if annotation not in neighborhood_annotation_dict.keys():
                        neighborhood_annotation_dict[annotation] = 1
                    else:
                        neighborhood_annotation_dict[annotation] += 1
                    neighborhood_annotations[pmid2] = neighborhood_annotation_dict
                            

print("Annotated pairs: " + str(counter_pairs))
print("Neigbors with annotations identified: " + str(counter_neighbors))
# compute recall, precision, F-measure and MAP
counter = 0
print("Computing F-measures and MAPs...")

recall_annotated = {}
recall_all = {}
precision_annotated = {}
precision_all = {}
f_measure_annotated = {}
f_measure_all = {}
average_precision_for_MAP_annotated = {}
average_precision_for_MAP_all = {}
shared_annotations = []
figure_data_lines = []

# go through each PMID
for pmid in annotations_pmid.keys():
    # check if PMID has annotations
    record_annotations = list(annotations_pmid[pmid].split("|"))
    record_annotations_count = len(record_annotations)
    neighborhood_annots = {}
    # if PMID has annotations
    if record_annotations_count > 0:
        shared_annotations_count = 0
        recall = 0
        precision = 0
        f_measure = 0
        empty_neighborhood = False
        average_precision_for_MAP = 0
        # check the annotations in the PMID's neighborhood (if any)
        if pmid in neighborhood_annotations.keys():
            counter += 1
            if counter / 100000 == int(counter / 100000):
                print("Read " + str(counter) + " statistics from records with annotated neighbors...")
            neighborhood_annots = neighborhood_annotations[pmid]
            # count those that are shared between the PMID and the neighborhood
            shared_annotations = list(set(neighborhood_annots.keys()) & set(record_annotations))
            shared_annotations_count = len(shared_annotations)
            # compute recall and precision based on that
            recall = shared_annotations_count / record_annotations_count
            precision = shared_annotations_count / len(neighborhood_annots.keys())
            # compute F-measure based on recall and precision
            if precision + recall > 0:
                f_measure = 2 * precision * recall / (precision + recall)
            else:
                f_measure = 0
            # here is the algorithm to compute the AP (for MAP)
            shared_annotation_counts = 0
            precision_for_MAP_sum = 0
            # for each annotation in the ranking (based on annotation counts)
            for i, annotation in enumerate(sorted(neighborhood_annots, key=neighborhood_annots.get, reverse=True)):
                # check if the predicted annotation is correct
                if annotation in shared_annotations:
                    # update the value of AP based on that
                    shared_annotation_counts += 1
                    precision_for_MAP = shared_annotation_counts / (i + 1)
                    precision_for_MAP_sum += precision_for_MAP
            # average the values to get the final AP
            average_precision_for_MAP = precision_for_MAP_sum / len(record_annotations)
        else:
            # flag if PMID has no neighbors
            empty_neighborhood = True
        # values of recall, precision, F-measure and AP are stored for later statistics
        if pmid in citation_counter_all.keys():
            total_citations = citation_counter_all[pmid]
            if total_citations in recall_all.keys():
                recall_all[total_citations].append(recall)
                average_precision_for_MAP_all[total_citations].append(average_precision_for_MAP)
            else:
                recall_all[total_citations] = [recall]
                average_precision_for_MAP_all[total_citations] = [average_precision_for_MAP]
            #if empty_neighborhood == False:
            if total_citations in precision_all.keys():
                precision_all[total_citations].append(precision)
            else:
                precision_all[total_citations] = [precision]
            if total_citations in f_measure_all.keys():
                f_measure_all[total_citations].append(f_measure)
            else:
                f_measure_all[total_citations] = [f_measure]
        # same as the previous block but for all connections, not just annotated ones
        if pmid in citation_counter_annotated.keys():
            total_annotated_citations = citation_counter_annotated[pmid]
            if total_annotated_citations in recall_annotated.keys():
                recall_annotated[total_annotated_citations].append(recall)
            else:
                recall_annotated[total_annotated_citations] = [recall]
            if total_annotated_citations in average_precision_for_MAP_annotated.keys():
                average_precision_for_MAP_annotated[total_annotated_citations].append(average_precision_for_MAP)
            else:
                average_precision_for_MAP_annotated[total_annotated_citations] = [average_precision_for_MAP]
            if total_annotated_citations in precision_annotated.keys():
                precision_annotated[total_annotated_citations].append(precision)
            else:
                precision_annotated[total_annotated_citations] = [precision]
            if total_annotated_citations in f_measure_annotated.keys():
                f_measure_annotated[total_annotated_citations].append(f_measure)
            else:
                f_measure_annotated[total_annotated_citations] = [f_measure]

# print statistics based on counts in the previous section
# the first output file is for recall, precision and F-measure
# the second is for MAP
print("Printing output to " + output_file_f_measure + "...")
f_out = open(output_file_f_measure, "w")
f_out.write("Connections\tRecall with annotated citations\tPrecision with annotated citations\tF-measure with annotated citations\tNumber of examples\tRecall with all\tPrecision with all\tF-measure with all\tNumber of examples\n")
print("Connections\tRecall with annotated citations\tPrecision with annotated citations\tF-measure with annotated citations\tNumber of examples\tRecall with all\tPrecision with all\tF-measure with all\tNumber of examples")

for i in range(1,max(recall_annotated.keys())+1):
    count1 = 0
    count2 = 0
    if i in recall_annotated.keys():
        recall_list_annotated = recall_annotated[i]
        average_recall_annotated = 100*sum(recall_list_annotated) / len(recall_list_annotated)
        count1 = len(recall_list_annotated)
        precision_list_annotated = precision_annotated[i]
        average_precision_annotated = 100*sum(precision_list_annotated) / len(precision_list_annotated)
        f_measure_list_annotated = f_measure_annotated[i]
        average_f_measure_annotated = 100*sum(f_measure_list_annotated) / len(f_measure_list_annotated)
    else:
        average_recall_annotated = "N/A"
        average_precision_annotated = "N/A"
        average_f_measure_annotated = "N/A"
    if i in recall_all.keys():
        recall_list_all = recall_all[i]
        average_recall_all = 100*sum(recall_list_all) / len(recall_list_all)
        count2 = len(recall_list_all)
        if i in precision_all.keys():
            precision_list_all = precision_all[i]
            average_precision_all = 100*sum(precision_list_all) / len(precision_list_all)
            f_measure_list_all = f_measure_all[i]
            average_f_measure_all = 100*sum(f_measure_list_all) / len(f_measure_list_all)
    else:
        average_recall_all = "N/A"
        average_precision_all = "N/A"
        average_f_measure_all = "N/A"
    f_out.write(str(i) + "\t" + str(average_recall_annotated) + "\t" + str(average_precision_annotated) + "\t" + str(average_f_measure_annotated) + "\t" + str(count1) + "\t" + str(average_recall_all) + "\t" + str(average_precision_all) + "\t" + str(average_f_measure_all) + "\t" + str(count2) + "\n")
    if i < 21:
        print(str(i) + "\t" + str(average_recall_annotated) + "\t" + str(average_precision_annotated) + "\t" + str(average_f_measure_annotated) + "\t" + str(count1) + "\t" + str(average_recall_all) + "\t" + str(average_precision_all) + "\t" + str(average_f_measure_all) + "\t" + str(count2))
        figure_data_lines.append(str(i) + "\t" + str(average_recall_annotated) + "\t" + str(average_precision_annotated) + "\t" + str(average_f_measure_annotated) + "\t")

print("Printing output to " + output_file_map + "...")

f_out = open(output_file_map, "w")

f_out.write("Connections\tAnnotation MAP with annotated citations\tNumber of examples\tAnnotation MAP with all\tNumber of examples\n")
print("Connections\tAnnotation MAP with annotated citations\tNumber of examples\tAnnotation MAP with all\tNumber of examples")


for i in range(1,max(average_precision_for_MAP_annotated.keys())+1):
    count1 = 0
    count2 = 0
    if i in average_precision_for_MAP_annotated.keys():
        average_precision_for_MAP_list_annotated = average_precision_for_MAP_annotated[i]
        mean_average_precision_for_MAP_annotated = 100*sum(average_precision_for_MAP_list_annotated) / len(average_precision_for_MAP_list_annotated)
        count1 = len(average_precision_for_MAP_list_annotated)
    else:
        mean_average_precision_for_MAP_annotated = "N/A"
    if i in average_precision_for_MAP_all.keys():
        average_precision_for_MAP_list_all = average_precision_for_MAP_all[i]
        mean_average_precision_for_MAP_all = 100*sum(average_precision_for_MAP_list_all) / len(average_precision_for_MAP_list_all)
        count2 = len(average_precision_for_MAP_list_all)
    else:
        mean_average_precision_for_MAP_all = "N/A"
    f_out.write(str(i) + "\t" + str(mean_average_precision_for_MAP_annotated) + "\t" + str(count1) + "\t" + str(mean_average_precision_for_MAP_all) + "\t" + str(count2) + "\n")
    if i < 21:
        print(str(i) + "\t" + str(mean_average_precision_for_MAP_annotated) + "\t" + str(count1) + "\t" + str(mean_average_precision_for_MAP_all) + "\t" + str(count2))
        figure_data_lines[i-1] = figure_data_lines[i-1] + str(mean_average_precision_for_MAP_annotated)

print("Printing output to " + output_figure_data + "...")
f_out = open(output_figure_data, "w")

f_out.write("Connections\tRecall\tPrecision\tF-measure\tMAP\n")
print("Connections\tRecall\tPrecision\tF-measure\tMAP")

for i in range(0,max(average_precision_for_MAP_annotated.keys())+1):
    if i < len(figure_data_lines):
        print(figure_data_lines[i])
        f_out.write(figure_data_lines[i] + "\n")



