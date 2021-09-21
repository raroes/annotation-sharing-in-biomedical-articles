#!/usr/bin/python3

# this script extract citations mentioned in the dbSNP database

import json
import bz2

output_file = "pmid_annotations_dbsnp.txt"

f_out = open(output_file, "w")

file_list1 = ['refsnp-chr' + str(i) for i in list(range(1,23)) + ['MT', 'X', 'Y']]


file_list = ["./data/" + base_file_name + ".json.bz2" for base_file_name in file_list1]

total_count = 0

for input_file in file_list:
    print(input_file)
    with bz2.BZ2File(input_file, 'rb') as f_in:
        for line in f_in:
            rs_obj = json.loads(line.decode('utf-8'))
            rsid = rs_obj['refsnp_id']
            citations = rs_obj['citations']
            for citation in citations:
                f_out.write(str(citation) + "\t" + rsid + "\n")
                total_count += 1

print("Total annotations: " + str(total_count))
