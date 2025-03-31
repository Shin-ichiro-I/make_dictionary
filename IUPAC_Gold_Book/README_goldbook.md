# Extract from IUPAC Gold BooK

## Attention

Note that the Gold Book is a dictionary compiled by the **International Union of Pure and Applied Chemistry (IUPAC)**, which sets international standards for compound names, but has not been revised since 2019.

The reliability of the registered contents seems to be higher than that of Wikidata, but the usability as a dictionary is worse than that of Wikidata due to many omissions in the recorded contents.

Therefore, it is intended to complement Wikidata.

```
from :https://iupac.org/what-we-do/databases/

IUPAC Gold Book

An interactive version of IUPAC Compendium of Chemical Terminology, informally known as the “Gold Book”. On these pages you will find a new browsable the alphabetical index, several thematic indexes, and a search function. Note that in the current version, the compendium of terms in not up-to-date and the latest IUPAC Recommendations and Colour Books have yet to be incorporated. Each term is correct based upon the source cited in its entry. However, the term’s definition may have since been superseded or may not reflect current chemical understanding. This version, launched July 2019, is the result of an update to the technical underpinnings of the Gold Book website to reflect advances in web technology. IUPAC Divisions are currently reviewing all entries and updates of the content will follow.
```

## Functional Design for Gold Book

1. Download all XML files with one file per phrase (7,096 files)
2. Analyze the contents of the downloaded XML file and extract necessary items
3. Save extracted data in JSON format

## How to extract XML files from the Gold Book (Procedure)

1. Get a list of all terms in JSON format by tapping directly on the ULR `https://goldbook.iupac.org/terms/index/all/json/`
2. Extract `term_id` from JSON
3. XML file call and download for each `term_id `https://goldbook.iupac.org/terms/view/{term_id}/xml/download`

## How to extract required items from an XML file

omission
