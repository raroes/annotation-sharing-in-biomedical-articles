# download UniProtKB annotations

curl -s ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz > ./data/idmapping_selected.tab.gz

gunzip -f ./data/idmapping_selected.tab.gz
