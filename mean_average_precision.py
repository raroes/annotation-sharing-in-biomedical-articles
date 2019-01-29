#!/usr/bin/python3

import sys

if len(sys.argv) > 1:
    input_citation_file = sys.argv[1]
    input_file = sys.argv[2]
else:
    input_citation_file = "pmid_citations.txt"
    input_file = "pmid_annotations.txt"

output_file_f_measure = "annotation_average_f_measure_based_on_connections.txt"
output_file_map = "annotation_map_based_on_connections.txt"

f_in = open(input_file, "r")

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

print("Reading citation data...")
neighborhood_annotations = {}
neighborhood_annotation_dict = {}
f_in = open(input_citation_file)

for line in f_in:
#for i in range(1,10000000):
#    line = f_in.readline()
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
        if pmid1 in annotations_pmid.keys():
            if pmid2 in annotations_pmid.keys():
                if pmid1 in citation_counter_annotated.keys():
                    citation_counter_annotated[pmid1] += 1
                else:
                    citation_counter_annotated[pmid1] = 1
                if pmid2 in citation_counter_annotated.keys():
                    citation_counter_annotated[pmid2] += 1
                else:
                    citation_counter_annotated[pmid2] = 1
                annotations1 = annotations_pmid[pmid1].split("|")
                annotations2 = annotations_pmid[pmid2].split("|")    
                for annotation in annotations2:
                    if pmid1 in neighborhood_annotations.keys():
                        neighborhood_annotation_dict = neighborhood_annotations[pmid1]
                    else:
                        neighborhood_annotation_dict = {}
                    #print(neighborhood_annotation_dict)
                    if annotation in neighborhood_annotation_dict.keys():
                        neighborhood_annotation_dict[annotation] += 1
                    else:
                        neighborhood_annotation_dict[annotation] = 1
                    neighborhood_annotations[pmid1] = neighborhood_annotation_dict
                for annotation in annotations1:
                    if pmid2 in neighborhood_annotations.keys():
                        neighborhood_annotation_dict = neighborhood_annotations[pmid2]
                    else:
                        neighborhood_annotation_dict = {}
                    if annotation not in neighborhood_annotation_dict.keys():
                        neighborhood_annotation_dict[annotation] = 1
                    else:
                        neighborhood_annotation_dict[annotation] += 1
                    neighborhood_annotations[pmid2] = neighborhood_annotation_dict
                            

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
for pmid in annotations_pmid.keys():
    record_annotations = list(annotations_pmid[pmid].split("|"))
    record_annotations_count = len(record_annotations)
    neighborhood_annots = {}
    counter += 1
    if counter / 100000 == int(counter / 100000):
        print("Read " + str(counter) + " record statistics...")
    if record_annotations_count > 0:
        shared_annotations_count = 0
        recall = 0
        precision = 0
        f_measure = 0
        empty_neighborhood = False
        average_precision_for_MAP = 0
        if pmid in neighborhood_annotations.keys():
            neighborhood_annots = neighborhood_annotations[pmid]
            shared_annotations = list(set(neighborhood_annots.keys()) & set(record_annotations))
            shared_annotations_count = len(shared_annotations)
            recall = shared_annotations_count / record_annotations_count
            precision = shared_annotations_count / len(neighborhood_annots.keys())
            if precision > 0 and recall > 0:
                f_measure = 2 * precision * recall / (precision + recall)
            else:
                f_measure = 0
            # MAP algorithm here
            shared_annotation_counts = 0
            precision_for_MAP_sum = 0
            for i, annotation in enumerate(sorted(neighborhood_annots, key=neighborhood_annots.get, reverse=True)):
                if annotation in shared_annotations:
                    shared_annotation_counts += 1
                    precision_for_MAP = shared_annotation_counts / (i + 1)
                    precision_for_MAP_sum += precision_for_MAP
                    #print(str(shared_annotation_counts) + "--" + str(i + 1) + "--" + str(precision))
            average_precision_for_MAP = precision_for_MAP_sum / len(record_annotations)
            for annotation in neighborhood_annots.keys():
                total_annotation_count = annotation_stats[annotation]
                neighborhood_annots[annotation] = neighborhood_annots[annotation] / total_annotation_count
        else:
            empty_neighborhood = True
        if pmid in citation_counter_all.keys():
            total_citations = citation_counter_all[pmid]
            if total_citations in recall_all.keys():
                recall_all[total_citations].append(recall)
                average_precision_for_MAP_all[total_citations].append(average_precision_for_MAP)
            else:
                recall_all[total_citations] = [recall]
                average_precision_for_MAP_all[total_citations] = [average_precision_for_MAP]
            if empty_neighborhood == False:
                if total_citations in precision_all.keys():
                    precision_all[total_citations].append(precision)
                    f_measure_all[total_citations].append(f_measure)
                else:
                    precision_all[total_citations] = [precision]
                    f_measure_all[total_citations] = [f_measure]
        if pmid in citation_counter_annotated.keys():
            total_annotated_citations = citation_counter_annotated[pmid]
            if total_annotated_citations in recall_annotated.keys():
                recall_annotated[total_annotated_citations].append(recall)
                average_precision_for_MAP_annotated[total_annotated_citations].append(average_precision_for_MAP)
                precision_annotated[total_annotated_citations].append(precision)
                f_measure_annotated[total_annotated_citations].append(f_measure)
            else:
                recall_annotated[total_annotated_citations] = [recall]
                average_precision_for_MAP_annotated[total_annotated_citations] = [average_precision_for_MAP]
                precision_annotated[total_annotated_citations] = [precision]
                f_measure_annotated[total_annotated_citations] = [f_measure]

print("Printing output to " + output_file_f_measure + "...")
f_out = open(output_file_f_measure, "w")
#print("Connections\tAnnotation coverage with annotated citations\tNumber of examples\tAnnotation coverage with all\tNumber of examples")
f_out.write("Connections\tRecall with annotated citations\tPrecision with annotated citations\tF-measure with annotated citations\tNumber of examples\tRecall with all\tPrecision with all\tF-measure with all\tNumber of examples\n")

for i in range(1,max(recall_annotated.keys())+1):
    count1 = 0
    count2 = 0
    if i in recall_annotated.keys():
        recall_list_annotated = recall_annotated[i]
        average_recall_annotated = sum(recall_list_annotated) / len(recall_list_annotated)
        count1 = len(recall_list_annotated)
        precision_list_annotated = precision_annotated[i]
        average_precision_annotated = sum(precision_list_annotated) / len(precision_list_annotated)
        f_measure_list_annotated = f_measure_annotated[i]
        average_f_measure_annotated = sum(f_measure_list_annotated) / len(f_measure_list_annotated)
    else:
        average_recall_annotated = "N/A"
        average_precision_annotated = "N/A"
        average_f_measure_annotated = "N/A"
    if i in recall_all.keys():
        recall_list_all = recall_all[i]
        average_recall_all = sum(recall_list_all) / len(recall_list_all)
        count2 = len(recall_list_all)
        if i in precision_all.keys():
            precision_list_all = precision_all[i]
            average_precision_all = sum(precision_list_all) / len(precision_list_all)
            f_measure_list_all = f_measure_all[i]
            average_f_measure_all = sum(f_measure_list_all) / len(f_measure_list_all)
    else:
        average_recall_all = "N/A"
        average_precision_all = "N/A"
        average_f_measure_all = "N/A"
    #print(str(i) + "\t" + str(average_percentage1) + "\t" + str(count1) + "\t" + str(average_percentage2) + "\t" + str(count2))
    f_out.write(str(i) + "\t" + str(average_recall_annotated) + "\t" + str(average_precision_annotated) + "\t" + str(average_f_measure_annotated) + "\t" + str(count1) + "\t" + str(average_recall_all) + "\t" + str(average_precision_all) + "\t" + str(average_f_measure_all) + "\t" + str(count2) + "\t" + "\n")

print("Printing output to " + output_file_map + "...")

f_out = open(output_file_map, "w")

f_out.write("Connections\tAnnotation MAP with annotated citations\tNumber of examples\tAnnotation MAP with all\tNumber of examples\n")


for i in range(1,max(average_precision_for_MAP_annotated.keys())+1):
    count1 = 0
    count2 = 0
    if i in average_precision_for_MAP_annotated.keys():
        average_precision_for_MAP_list_annotated = average_precision_for_MAP_annotated[i]
        mean_average_precision_for_MAP_annotated = sum(average_precision_for_MAP_list_annotated) / len(average_precision_for_MAP_list_annotated)
        count1 = len(average_precision_for_MAP_list_annotated)
    else:
        mean_average_precision_for_MAP_annotated = "N/A"
    if i in average_precision_for_MAP_all.keys():
        average_precision_for_MAP_list_all = average_precision_for_MAP_all[i]
        mean_average_precision_for_MAP_all = sum(average_precision_for_MAP_list_all) / len(average_precision_for_MAP_list_all)
        count2 = len(average_precision_for_MAP_list_all)
    else:
        mean_average_precision_for_MAP_all = "N/A"
    #print(str(i) + "\t" + str(average_percentage1) + "\t" + str(count1) + "\t" + str(average_percentage2) + "\t" + str(count2))
    f_out.write(str(i) + "\t" + str(mean_average_precision_for_MAP_annotated) + "\t" + str(count1) + "\t" + str(mean_average_precision_for_MAP_all) + "\t" + str(count2) + "\t" + "\n")

