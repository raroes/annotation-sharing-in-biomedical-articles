# this script executes all the steps necessary fot the analysis
# the only steps missing are the download of MEDLINE and the BC2GN datasets, which can be done separately

# directory where the scripts will be located
export BASE_DIR="."
# whether to download the data files or not
export DOWNLOAD_FILES=0

if [ $DOWNLOAD_FILES -eq 1 ]; then

	if [ ! -d "$DIRECTORY" ]; then
		mkdir $BASE_DIR/data
	fi

	# download mapping from DOI to PMID
	echo $BASE_DIR/download_pmid_doi_mapping.sh
	$BASE_DIR/download_pmid_doi_mapping.sh

	# download citations
	echo $BASE_DIR/download_citations.sh
	$BASE_DIR/download_citations.sh

	# download gene2pubmed database
	echo $BASE_DIR/download_gene2pubmed.sh
	$BASE_DIR/download_gene2pubmed.sh

	# download uniprot annotations
	echo $BASE_DIR/download_uniprot.sh
	$BASE_DIR/download_uniprot.sh

        # download MeSH tree
        echo $BASE_DIR/download_mesh_tree.sh
        $BASE_DIR/download_mesh_tree.sh

        # download dbSNP mutations
	echo $BASE_DIR/download_dbsnp.py
	$BASE_DIR/download_dbsnp.py

fi

# map citations from DOI to PMID
echo $BASE_DIR/map_doi_citations_to_pmid.py
$BASE_DIR/map_doi_citations_to_pmid.py

# create the randomized network
echo $BASE_DIR/create_shuffled_network.py
$BASE_DIR/create_shuffled_network.py

# create second-degree network
echo $BASE_DIR/sort_citations.py
$BASE_DIR/sort_citations.py
echo $BASE_DIR/expand_citations.py
$BASE_DIR/expand_citations.py

# read gene2pubmed annotations
echo $BASE_DIR/read_gene_annotations_gene2pubmed.py
$BASE_DIR/read_gene_annotations_gene2pubmed.py

# read UniprotKB annotations
echo $BASE_DIR/read_gene_annotations_uniprot.py
$BASE_DIR/read_gene_annotations_uniprot.py

## parse dbSNP mutations
echo $BASE_DIR/parse_mutation_annotations_dbsnp.py
$BASE_DIR/parse_mutation_annotations_dbsnp.py

## read PMIDs in MEDLINE
echo $BASE_DIR/parse_medline_for_pmids.py
$BASE_DIR/parse_medline_for_pmids.py

# read list of MeSH terms
echo $BASE_DIR/parse_medline_for_mesh.py
$BASE_DIR/parse_medline_for_mesh.py

## read MeSH annotations
echo $BASE_DIR/read_mesh_annotations.py
$BASE_DIR/read_mesh_annotations.py

## gene2pubmed

## compute F-measure and MAP for the first-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt

## compute F-measure and MAP for the randomized network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt

## compute F-measure and MAP for the second-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt

## Uniprot

## compute F-measure and MAP
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_uniprot.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_uniprot.txt 

## compute F-measure and MAP for the randomized network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_uniprot.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_uniprot.txt

## compute F-measure and MAP for the second-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_uniprot.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_uniprot.txt

## dbSNP

## compute F-measure and MAP for the first-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_dbsnp.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_dbsnp.txt

## compute F-measure and MAP for the randomized network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_dbsnp.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_dbsnp.txt

## compute F-measure and MAP for the second-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_dbsnp.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_dbsnp.txt

## MESH

## compute F-measure and MAP
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_mesh.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_mesh.txt

## compute F-measure and MAP for the randomized network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_mesh.txt

## compute F-measure and MAP for the second-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_mesh.txt


## compute coverage of the gene2pubmed network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_citations.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_citations.txt

## compute coverage of the gene2pubmed second-degree network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_citations_second_degree.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_citations_second_degree.txt

## compute coverage of the UniProt network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_uniprot.txt $BASE_DIR/pmid_citations.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_uniprot.txt $BASE_DIR/pmid_citations.txt

## compute coverage of the UniProt second-degree network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_uniprot.txt $BASE_DIR/pmid_citations_second_degree.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_uniprot.txt $BASE_DIR/pmid_citations_second_degree.txt


## compute coverage of the dbSNP network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_dbsnp.txt $BASE_DIR/pmid_citations.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_dbsnp.txt $BASE_DIR/pmid_citations.txt

## compute coverage of the dbSNP second-degree network
echo $BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_dbsnp.txt $BASE_DIR/pmid_citations_second_degree.txt
$BASE_DIR/neighborhood_annotation_statistics_all_medline.py $BASE_DIR/pmid_annotations_dbsnp.txt $BASE_DIR/pmid_citations_second_degree.txt

## read BC2GN annotations
echo $BASE_DIR/read_gene_annotations_bc2.py
$BASE_DIR/read_gene_annotations_bc2.py

## compute individual-document recall values for BC2GN
echo $BASE_DIR/bc2gn_recall.py
$BASE_DIR/bc2gn_recall.py

## compute individual-document recall values for BC2GN with second degree network
echo $BASE_DIR/bc2gn_recall.py $BASE_DIR/pmid_citations_second_degree.txt
$BASE_DIR/bc2gn_recall.py $BASE_DIR/pmid_citations_second_degree.txt

## compute individual-document recall values for BCG2N with the randomized network
echo $BASE_DIR/bc2gn_recall.py $BASE_DIR/pmid_citations_shuffled.txt
$BASE_DIR/bc2gn_recall.py $BASE_DIR/pmid_citations_shuffled.txt

## compute MAP for BC2GN
echo $BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt
$BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt

## compute MAP for BC2GN using the randomized network
echo $BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt
$BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt

## using the second-degree network
echo $BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt
$BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations_gene2pubmed.txt $BASE_DIR/pmid_annotations_bc2.txt

## repeat the same analysis done for BC2GN but for other reference datasets
echo $BASE_DIR/create_reference_annotations.py
$BASE_DIR/create_reference_annotations.py

## compute MAP for L1000
echo $BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotationsi_mesh.txt $BASE_DIR/pmid_annotations_L1000.txt
$BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_mesh.txt $BASE_DIR/pmid_annotations_L1000.txt

## compute MAP for NLM2007
echo $BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_mesh.txt $BASE_DIR/pmid_annotations_NLM2007.txt
$BASE_DIR/bc2gn_mean_average_precision.py $BASE_DIR/pmid_citations.txt $BASE_DIR/pmid_annotations_mesh.txt $BASE_DIR/pmid_annotations_NLM2007.txt
