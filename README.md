# Biomedical articles share annotations with their citation neighborhood

Author: Raul Rodriguez-Esteban

Reference: Rodriguez-Esteban R. Biomedical articles share annotations with their citation neighbors. BMC Bioinformatics. 2021 Feb 26;22(1):95. 

Paper link: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-021-04044-4

The entire analysis can be run using the script *run_all.sh*, which contains the sequence of scripts that needs to be followed.
The only thing missing in the *run_all.sh* script is the download of the MEDLINE, NLM2007, L1000 and BC2GN datasets.

Below you can find a brief description of some of the files in this repository.

#### Download data files:

* *download_citations.sh*: download citations from the Open Citation Index. The URL has to be adjusted for newer releases of the data.
* *download_gene2pubmed.sh*: download the gene2pubmed database
* *download_pmid_doi_mapping.sh*: download the PMID-PMC-DOI mappings from EBI
* *download_uniprot.sh*: download the UniProtKB annotations
* *download_mesh_tree.sh*: download MeSH tree structure

#### Processing data files:

* *read_gene_annotations_uniprot.py*
* *read_gene_annotations_gene2pubmed.py*
* *read_mutation_annotations_dbsnp.py*
* *read_gene_annotations_bc2.py*
* *read_mesh_annotations.py*

* *mean_average_precision.py*: main script computing recall, precision and MAP

#### For the BC2GN analysis:

* *bc2gn_mean_average_precision.py*: MAP values for BC2GN annotations
* *bc2gn_recall.py*: recall values for BC2GN annotations

#### Additional files:

* *create_reference_annotations.py*: processes the reference datasets NLM2007 and L1000
* *create_shuffled_network.py*: creates a shuffled version of the original network
* *map_doi_citations_to_pmid.py*: map citation pairs in DOI format to PMID using the EBI mapping data
* *neighborhood_annotation_statistics_all_medline.py*: network neighbor stats for all MEDLINE records
* *parse_medline_for_mesh.py*: list all MeSH major topic annotations in MEDLINE
* *parse_medline_for_pmids.py*: list all MEDLINE PMIDs
