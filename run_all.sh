export BASE_DIR="."
export DOWNLOAD_FILES=1

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

# compute F-measure and MAP for the first-degree network
echo $BASE_DIR/mean_average_precision.py
$BASE_DIR/mean_average_precision.py

# compute F-measure and MAP for the randomized network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_shuffled.txt $BASE_DIR/pmid_annotations.txt

# compute F-measure and MAP for the second-degree network
echo $BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations.txt
$BASE_DIR/mean_average_precision.py $BASE_DIR/pmid_citations_second_degree.txt $BASE_DIR/pmid_annotations.txt

# read UniprotKB annotations
echo $BASE_DIR/read_gene_annotations_uniprot.py
$BASE_DIR/read_gene_annotations_uniprot.py

# compute F-measure and MAP
echo $BASE_DIR/mean_average_precision.py
$BASE_DIR/mean_average_precision.py
