#!/usr/bin/python3

# this script reads gene annotations from the UniProtKB database
input_file = "./data/idmapping_selected.tab"
output_file = "pmid_annotations.txt"


print("Processing UniProtKB annotations")

# open the data input file
f = open(input_file, 'r')

pmids_per_gene_id = {}
gene_ids_per_pmid = {}
gene_id_list = {}
total_annotations = 0
pmids = {}
# read all lines
print("Reading annotations...")
for line in f:
    line = line[:-1]
    # take information regarding species, gene ID and PMID
    data = line.split("\t")
    species = data[12]
    gene_id = data[2]
    pmid_data = data[15].split("; ")
    # only entries corresponding to human genes are selected
    if species == "9606" and gene_id != "" and len(pmid_data) > 0:
        for pmid in pmid_data:
            # keep a list of all unique PMIDs
            pmids[pmid] = 1
            # keep a list of all unique gene IDs
            if gene_id not in gene_id_list.keys():
                gene_id_list[gene_id] = 1
            # for every gene ID, keep a list of all PMIDs in which it was annotated
            if gene_id not in pmids_per_gene_id:
                pmids_per_gene_id[gene_id] = [pmid]
                total_annotations += 1
            else:
                if pmid not in pmids_per_gene_id[gene_id]:
                    pmids_per_gene_id[gene_id].append(pmid)
                    total_annotations += 1
            # for every PMID, keep a list of all gene IDs that were annotated
            if pmid not in gene_ids_per_pmid:
                gene_ids_per_pmid[pmid] = [gene_id]
            else:
                if gene_id not in gene_ids_per_pmid[pmid]:
                    gene_ids_per_pmid[pmid].append(gene_id)

print("Total (human) annotations: " + str(total_annotations))
print("Total number of genes with annotations: " + str(len(gene_id_list.keys())))
print("Total articles annotated: " + str(len(pmids.keys())))

# count the number of PMIDs associated to each gene ID
pmids_per_gene_id_count = {}
for gene_id in pmids_per_gene_id.keys():
   number_of_pmids = len(pmids_per_gene_id[gene_id])
   if number_of_pmids not in pmids_per_gene_id_count.keys():
       pmids_per_gene_id_count[number_of_pmids]=0
   pmids_per_gene_id_count[number_of_pmids]+=1

# write for each PMID all the gene IDs that were found
print("Writing output file...")

f_out = open(output_file, "w")
for pmid in gene_ids_per_pmid.keys():
    f_out.write(pmid + "\t" + "|".join(gene_ids_per_pmid[pmid]) + "\n")

print("Finished writing output file.\n")
