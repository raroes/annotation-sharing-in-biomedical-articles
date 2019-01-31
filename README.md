# Prediction of annotations using the citation network

#### For the main analysis the order of execution of the scripts is the following, first:

#### Download data files:

### * *download_citations.sh*: download citations from the Open Citation Index
### * *download_gene2pubmed.sh*: download the gene2pubmed database
### * *download_goa.sh*: download the Gene Ontology Annotation database
### * *download_pmid_doi_mapping.sh*: download the PMID-PMC-DOI mappings from EBI
### * *download_uniprot.sh*: download the UniProtKB annotations
### * *download_mesh_tree.sh*: download MeSH tree structure

#### Then, one of these scripts:

### * *read_gene_annotations_uniprot.py*
### * *read_gene_annotations_gene2pubmed.py*
### * *read_gene_annotations_goa.py*
### * *read_gene_annotations_bc2.py*
### * *read_mesh_annotations.py*

#### Then:

### * *mean_average_precision.py*

#### For the BC2GN analysis:

### * *bc2gn_mean_average_precision.py*: MAP values for BC2GN annotations
### * *bc2gn_recall.py*: recall values for BC2GN annotations

#### Additional files:

### * *create_second_degree_network.py*: creates the second-degree citation network
### * *create_shuffled_network.py*: creates a shuffled version of the original network
### * *map_doi_citations_to_pmid*: map citation pairs in DOI format to PMID using the EBI mapping data
### * *neighborhood_annotation_statistics.py*: network neighbor stats for annotated records
### * *neighborhood_annotation_statistics_all_medline.py*: network neighbor stats for all MEDLINE records
### * *parse_medline_for_mesh.py*: list all MeSH major topic annotations in MEDLINE
### * *parse_medline_for_pmids.py*: list all MEDLINE PMIDs
