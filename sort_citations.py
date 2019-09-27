#!/usr/bin/python3

# duplicate citations by reversing each citation pair
# this allows the creation of the second degree network by the next step (expand)

input_file = "pmid_citations.txt"
output_file = "pmid_citations_sorted.txt"

f_in = open(input_file, "r")

pair_pmids = {}

print("Reading citations...")
counter = 0
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = int(data[0])
    pmid2 = int(data[1])
    if pmid1 not in pair_pmids.keys():
        pair_pmids[pmid1] = [pmid2]
    else:
        pair_pmids[pmid1].append(pmid2)
    if pmid2 not in pair_pmids.keys():
        pair_pmids[pmid2] = [pmid1]
    else:
        pair_pmids[pmid2].append(pmid1)
    counter += 1
    if counter / 10000000 == int(counter / 10000000):
        print("Read " + str(counter) + " citations.")

print("Citations read.")
print("Writing sorted citations...")

f_out = open(output_file, "w")

for pmid1 in pair_pmids.keys():
    for pmid2 in pair_pmids[pmid1]:
        f_out.write(str(pmid1) + "\t" + str(pmid2) + "\n")
