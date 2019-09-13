# download PMID-PMCID-DOI mapping from EBI

curl -s ftp://ftp.ebi.ac.uk/pub/databases/pmc/DOI/PMID_PMCID_DOI.csv.gz > ./data/PMID_PMCID_DOI.csv.gz

gunzip -f ./data/PMID_PMCID_DOI.csv.gz
