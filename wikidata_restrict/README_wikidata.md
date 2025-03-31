# Extract from Wikidata

## Building a python environment

Installed python-3.7.4 after installing penv
```python-3.7.4
pyenv install 3.7.4
```

Building a virtual environment
```venv
python3..7 -m venv venv
```

Activate Virtual Environment
```venv activation
venv\Scripts\activate # windows
source venv/bin/activate # Mac, Linux
```

package installation
```pandas, request
pip install pandas==1.3.5 requests==2.31.0
```

## Python Execution Command

Features
- Data download takes time and can be downloaded in installments
- `start_index` : First `index` of words to be extracted
- `stop_index` : The `index` of the word or phrase that completes the extraction
- Since data is output to a CSV file every 5,000 words, the difference between `start_index` and `stop_index` should be a multiple of 5,000

```Execution code example
poetry run python main_restrict.py {start_index} {stop_index}
poetry run python main_restrict.py 1 40000
```


## Functional Design for Wikidata

1. scope of the dictionary: specializing in polymer chemistry (later expanded to include organic and inorganic chemistry)
2. Data to be extracted from Wikidata:
    - Names of chemical substances (both Japanese and English)
    - Synonyms and synonyms of chemicals (idioms and IUPAC names are also considered synonyms)
    - superordinate and subordinate concepts
3. Output dictionary format: CSV format
4. Data extraction and processing tools: Python

## Procedure for extraction from Wikidata

1. get a list of items in a SPARQL query

    ```get_item_list function
    def get_item_list(offset, limit=100):

        query = f"""
        SELECT?item WHERE {{
        ?item wdt:P279/wdt:P279* wd:Q81163.  # polymer
        }}
        """
        url = 'https://query.wikidata.org/sparql'
        headers = {
            'User-Agent': 'MyMakeDic/1.0 (xxxxx@xxxxx.co.jp)' # Note that if you do not enter your e-mail real name, a timeout will occur!
            }
        params = {
            'query': query,
            'format': 'json'
        }
    ```

2. Extract detailed data for each item id with Wikidata API

    ```get_item_data function
    def get_item_data(item_ids):
        url = 'https://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbgetentities',
            'ids': '|'.join(item_ids),  # Specify multiple IDs separated by |
            'languages': 'ja|en',
            'props': 'labels|aliases|claims',
            'format': 'json'
        }
    ```  

3. Output extracted data to file

    ```Outline only
    # extracted data item
    'http://www.wikidata.org/entity/' + item_id,
    data['labels'].get('ja', {}).get('value'),
    data['labels'].get('en', {}).get('value'),
    altLabel_ja = [alias['value'] for alias in data['aliases']['ja']]
    altLabel_en = [alias['value'] for alias in data['aliases']['en']]
    claims_p31 = data.get('claims', {}).get('P31')

    # Composition of csv files
    df = pd.DataFrame(all_data, columns=[
                            "item", "label_ja", "label_en", "altLabel_ja", "altLabel_en", "instance of"
                        ])

    ```

### Number of items in Wikidata (2025.02.19)

- Searchable via the Wikidata Query Service :https://query.wikidata.org/

```Query for item count
SELECT (COUNT(?item) AS ?count) WHERE {
?item wdt:P31/wdt:P279* wd:Q178593 .  # Count items whose instance (P31) is a polymer or its subclass (P279)
}
```

- Q178593 (macromolecule): 1148429 → 1148917
- Q81163（polymer）: 1148916


### Reference

#### SPARQL Query Properties

```- wdt:P460 (synonym): property representing the most direct synonym
- wdt:P1889 (synonyms): Represents words that have approximately the same meaning
- wdt:P1424 (alias): Used to refer to something by a different name, which may include a conventional name, abbreviation, product name, etc.
- wdt:P1709 (brand): Represents a trade name and may include trade names of polymeric materials
- IUPAC and conventional names are considered synonyms if they refer to the same substance
- Abbreviations are considered synonyms of the official name
- Product names are considered synonyms of the official (or customary) name
- wdt:P31 :instance of
- wdt:P279 :subclass of```
