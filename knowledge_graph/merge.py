import json
import pandas as pd

# Read Gold Book JSON file
with open("C:/Users/LPC_0099/Documents/python_program/make_dictionary/IUPAC_Gold_Book/goldbook_terms.json", "r", encoding="utf-8") as f:
    goldbook_data = json.load(f)

# Import Wikidata CSV files
wikidata_df = pd.read_csv("C:/Users/LPC_0099/Documents/python_program/make_dictionary/wikidata_restrict/chemical_data_api_Q81163_高分子_1-20000.csv")
wikidata_df = wikidata_df.drop_duplicates(subset='item', keep='first')  # Delete duplicate records if any
wikidata_df = wikidata_df[wikidata_df['label_en'].notna()]

# List to store knowledge graph data
knowledge_graph = []

# For each entry in the Gold Book
for gb_entry in goldbook_data:
    gb_title = gb_entry["title"]
    # Search Wikidata for entries matching label_en
    wd_entry = wikidata_df[wikidata_df["label_en"] == gb_title]
    # Merge any matching entries
    if len(wd_entry) > 0:
        knowledge_graph.append({
            "@id": wd_entry["item"].iloc[0],  # Wikidata IDs are preferred
            "title": gb_title,
            "definitions": gb_entry.get("definitions", []),
            # ウィキデータのラベル_ja、altLabel_ja、altLabel_jaを追加する。
            "label_ja": wd_entry["label_ja"].values[0] if pd.notna(wd_entry["label_ja"].values[0]) else "",
            "altLabel_ja": wd_entry["altLabel_ja"].values[0] if pd.notna(wd_entry["altLabel_ja"].values[0]) else "",
            "altLabel_en": wd_entry["altLabel_en"].values[0] if pd.notna(wd_entry["altLabel_en"].values[0]) else "",
            # Add other Gold Book information
            "id": gb_entry["id"],
            "altLabels": gb_entry.get("altLabels", []),
            "relatedTerms": gb_entry.get("relatedTerms", []),
            "chemicals": gb_entry.get("chemicals", []),
            "abbrevs": gb_entry.get("abbrevs", []),
            "contains": gb_entry.get("contains", []),
            "synonyms": gb_entry.get("synonyms", []),
            "contexts": gb_entry.get("contexts", []),
            "math": gb_entry.get("math", []),
            "symbols": gb_entry.get("symbols", []),
            "processes": gb_entry.get("processes", []),
        })
    # Add Gold Book entry if no matching entry
    else:
        knowledge_graph.append({
            "@id": gb_entry["id"],
            "title": gb_title,
            "definitions": gb_entry.get("definitions", []),
            # Add empty label_en, altLabel_en, altLabel_en which have no entry in Gold Book
            "label_ja": "",
            "altLabel_ja": "",
            "altLabel_en": "",
            # Add other Gold Book information
            "altLabels": gb_entry.get("altLabels", []),
            "relatedTerms": gb_entry.get("relatedTerms", []),
            "chemicals": gb_entry.get("chemicals", []),
            "abbrevs": gb_entry.get("abbrevs", []),
            "contains": gb_entry.get("contains", []),
            "synonyms": gb_entry.get("synonyms", []),
            "contexts": gb_entry.get("contexts", []),
            "math": gb_entry.get("math", []),
            "symbols": gb_entry.get("symbols", []),
            "processes": gb_entry.get("processes", []),
        })

# Wikidata entries added that are not in the Gold Book
for index, wd_row in wikidata_df.iterrows():
    wd_label = wd_row["label_en"]
    # Check for entries matching the Gold Book title
    if not any(gb_entry["title"] == wd_label for gb_entry in goldbook_data):
        knowledge_graph.append({
            "@id": wd_row["item"],
            "title": wd_label,
            "definitions": "",  # Add empty because there is no entry in wikidata
            # Add wiki data label_en, altLabel_en, altLabel_en
            "label_ja": wd_row["label_ja"] if pd.notna(wd_row["label_ja"]) else "",
            "altLabel_ja": wd_row["altLabel_ja"] if pd.notna(wd_row["altLabel_ja"]) else "",
            "altLabel_en": wd_row["altLabel_en"] if pd.notna(wd_row["altLabel_en"]) else "",
            # Add empty entries for other items that are in the Gold Book but not in Wikidata
            "id": "",
            "altLabels": "",
            "relatedTerms": "",
            "chemicals": "",
            "abbrevs": "",
            "contains": "",
            "synonyms": "",
            "contexts": "",
            "math": "",
            "symbols": "",
            "processes": "",
        })

# Save in JSON-LD format
with open("knowledge_graph_test.jsonld", "w", encoding="utf-8") as f:
    json.dump(knowledge_graph, f, ensure_ascii=False, indent=2)
