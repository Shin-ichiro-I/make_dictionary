# make_dictionary

Powered by Gemini Advanced 2.0 Flash

## Data Source

- [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)
- [IUPAC Gold Book](https://goldbook.iupac.org/)

## Total Design of Making Dictionary

1. [Extract from Wikidata](wikidata_restrict/README_wikidata.md)
2. [Extract from IUPAC Gold Book](IUPAC_Gold_Book/README_goldbook.md)
3. [Merge Wikidata and Gold Book](knowledge_graph/merge.py)
4. Make original knowledegraph with above data

### Othre Possible Data Source

- [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- 高分子辞典 :No electronic dictionary provided (need to digitize ourselves)
- 岩波 理化学辞典 :No electronic dictionary provided (need to digitize ourselves)
- CRC Handbook of Chemistry and Physics :No electronic dictionary provided (need to digitize ourselves)
- [Polyinfo](https://polymer.nims.go.jp/) :Prohibited by machine download such as scraping
