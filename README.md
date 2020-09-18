# Annotation sharing using the citation network

The entire analysis can be run using the script *run_all.sh*, which contains the sequence of scripts that needs to be followed.
The only thing missing in the *run_all.sh* script is the download of the MEDLINE and BC2GN datasets.

Below you can find a brief description of some of the files in this repository.

#### Download data files:

* *download_citations.sh*: download citations from the Open Citation Index
* *download_gene2pubmed.sh*: download the gene2pubmed database
* *download_goa.sh*: download the Gene Ontology Annotation database
* *download_pmid_doi_mapping.sh*: download the PMID-PMC-DOI mappings from EBI
* *download_uniprot.sh*: download the UniProtKB annotations
* *download_mesh_tree.sh*: download MeSH tree structure

#### Processing data files:

* *read_gene_annotations_uniprot.py*
* *read_gene_annotations_gene2pubmed.py*
* *read_mutation_annotations_dbsnp.py*
* *read_gene_annotations_bc2.py*
* *read_mesh_annotations.py*

* *mean_average_precision.py*: main script computing recall, precision, F-measure and MAP

#### For the BC2GN analysis:

* *bc2gn_mean_average_precision.py*: MAP values for BC2GN annotations
* *bc2gn_recall.py*: recall values for BC2GN annotations

#### Additional files:

* *create_shuffled_network.py*: creates a shuffled version of the original network
* *map_doi_citations_to_pmid.py*: map citation pairs in DOI format to PMID using the EBI mapping data
* *neighborhood_annotation_statistics_all_medline.py*: network neighbor stats for all MEDLINE records
* *parse_medline_for_mesh.py*: list all MeSH major topic annotations in MEDLINE
* *parse_medline_for_pmids.py*: list all MEDLINE PMIDs
